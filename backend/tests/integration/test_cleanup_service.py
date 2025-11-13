"""
Tests for automatic environment cleanup service.
"""

import asyncio
import pytest

from src.platform.isolationEngine.cleanup import EnvironmentCleanupService
from src.platform.db.schema import RunTimeEnvironment


class TestCleanupService:
    """Test automatic cleanup of expired environments."""

    @pytest.mark.asyncio
    async def test_cleanup_removes_expired_environment(
        self, core_isolation_engine, environment_handler, session_manager
    ):
        """Test that cleanup service removes expired environments."""
        # Create environment with very short TTL (1 second)
        env = core_isolation_engine.create_environment(
            template_schema="slack_default",
            ttl_seconds=1,
            created_by="test_user",
            impersonate_user_id="U01AGENBOT9",
        )

        # Verify environment and schema exist
        assert environment_handler.schema_exists(env.schema_name)

        with session_manager.with_meta_session() as session:
            db_env = (
                session.query(RunTimeEnvironment)
                .filter(RunTimeEnvironment.id == env.environment_id)
                .one()
            )
            assert db_env.status == "ready"

        # Start cleanup service with 1 second interval
        cleanup_service = EnvironmentCleanupService(
            session_manager=session_manager,
            environment_handler=environment_handler,
            interval_seconds=1,
        )
        await cleanup_service.start()

        # Wait for TWO cleanup cycles (two-phase: mark expired, then delete)
        # 1s for TTL + 1s cycle 1 (mark expired) + 1s cycle 2 (delete) + buffer = 3.5s
        await asyncio.sleep(3.5)

        # Stop cleanup service
        await cleanup_service.stop()

        # Verify environment was cleaned up
        assert not environment_handler.schema_exists(env.schema_name)

        with session_manager.with_meta_session() as session:
            db_env = (
                session.query(RunTimeEnvironment)
                .filter(RunTimeEnvironment.id == env.environment_id)
                .one()
            )
            assert db_env.status == "deleted"

    @pytest.mark.asyncio
    async def test_cleanup_ignores_non_expired_environment(
        self, core_isolation_engine, environment_handler, session_manager
    ):
        """Test that cleanup service does not remove non-expired environments."""
        # Create environment with long TTL (3600 seconds = 1 hour)
        env = core_isolation_engine.create_environment(
            template_schema="slack_default",
            ttl_seconds=3600,
            created_by="test_user",
            impersonate_user_id="U01AGENBOT9",
        )

        # Verify environment exists
        assert environment_handler.schema_exists(env.schema_name)

        # Start cleanup service
        cleanup_service = EnvironmentCleanupService(
            session_manager=session_manager,
            environment_handler=environment_handler,
            interval_seconds=1,
        )
        await cleanup_service.start()

        # Wait for at least one cleanup cycle
        await asyncio.sleep(1.5)

        # Stop cleanup service
        await cleanup_service.stop()

        # Verify environment still exists (not expired)
        assert environment_handler.schema_exists(env.schema_name)

        with session_manager.with_meta_session() as session:
            db_env = (
                session.query(RunTimeEnvironment)
                .filter(RunTimeEnvironment.id == env.environment_id)
                .one()
            )
            assert db_env.status == "ready"

        # Cleanup
        environment_handler.drop_schema(env.schema_name)

    @pytest.mark.asyncio
    async def test_cleanup_service_lifecycle(
        self, core_isolation_engine, environment_handler, session_manager
    ):
        """Test cleanup service start/stop lifecycle."""
        # Create environment with 1 second TTL
        env = core_isolation_engine.create_environment(
            template_schema="slack_default",
            ttl_seconds=1,
            created_by="test_user",
            impersonate_user_id="U01AGENBOT9",
        )

        # Create cleanup service with fast interval
        cleanup_service = EnvironmentCleanupService(
            session_manager=session_manager,
            environment_handler=environment_handler,
            interval_seconds=1,
        )

        # Start the service
        await cleanup_service.start()
        assert cleanup_service._running is True

        # Wait for TWO cleanup cycles (mark expired + delete)
        await asyncio.sleep(3.5)

        # Stop the service
        await cleanup_service.stop()
        assert cleanup_service._running is False

        # Verify environment was cleaned up
        assert not environment_handler.schema_exists(env.schema_name)

    @pytest.mark.asyncio
    async def test_cleanup_handles_multiple_expired_environments(
        self, core_isolation_engine, environment_handler, session_manager
    ):
        """Test that cleanup service handles multiple expired environments."""
        # Create 3 environments with short TTL
        envs = []
        for i in range(3):
            env = core_isolation_engine.create_environment(
                template_schema="slack_default",
                ttl_seconds=1,
                created_by=f"test_user_{i}",
                impersonate_user_id="U01AGENBOT9",
            )
            envs.append(env)

        # Verify all exist
        for env in envs:
            assert environment_handler.schema_exists(env.schema_name)

        # Start cleanup service
        cleanup_service = EnvironmentCleanupService(
            session_manager=session_manager,
            environment_handler=environment_handler,
            interval_seconds=1,
        )
        await cleanup_service.start()

        # Wait for TWO cleanup cycles for all environments
        await asyncio.sleep(3.5)

        # Stop cleanup service
        await cleanup_service.stop()

        # Verify all were cleaned up
        for env in envs:
            assert not environment_handler.schema_exists(env.schema_name)

    @pytest.mark.asyncio
    async def test_cleanup_handles_failed_schema_drop_gracefully(
        self, core_isolation_engine, environment_handler, session_manager
    ):
        """Test that cleanup continues even if one schema drop fails."""
        # Create 2 environments with short TTL
        env1 = core_isolation_engine.create_environment(
            template_schema="slack_default",
            ttl_seconds=1,
            created_by="test_user_1",
            impersonate_user_id="U01AGENBOT9",
        )

        env2 = core_isolation_engine.create_environment(
            template_schema="slack_default",
            ttl_seconds=1,
            created_by="test_user_2",
            impersonate_user_id="U01AGENBOT9",
        )

        # Manually drop env1 schema to simulate failure
        environment_handler.drop_schema(env1.schema_name)

        # Start cleanup service
        cleanup_service = EnvironmentCleanupService(
            session_manager=session_manager,
            environment_handler=environment_handler,
            interval_seconds=1,
        )
        await cleanup_service.start()

        # Wait for TWO cleanup cycles
        await asyncio.sleep(3.5)

        # Stop cleanup service
        await cleanup_service.stop()

        # Verify env1 marked as cleanup_failed, env2 deleted
        with session_manager.with_meta_session() as session:
            db_env1 = (
                session.query(RunTimeEnvironment)
                .filter(RunTimeEnvironment.id == env1.environment_id)
                .one()
            )
            # Should be marked as failed since schema already dropped
            assert db_env1.status in ["cleanup_failed", "deleted"]

            db_env2 = (
                session.query(RunTimeEnvironment)
                .filter(RunTimeEnvironment.id == env2.environment_id)
                .one()
            )
            assert db_env2.status == "deleted"

        # env2 schema should be gone
        assert not environment_handler.schema_exists(env2.schema_name)

    @pytest.mark.asyncio
    async def test_cleanup_phase_one_marks_as_expired(
        self, core_isolation_engine, environment_handler, session_manager
    ):
        """Test that phase 1 marks ready environments as expired when TTL passes."""
        # Create environment with short TTL
        env = core_isolation_engine.create_environment(
            template_schema="slack_default",
            ttl_seconds=1,
            created_by="test_user",
            impersonate_user_id="U01AGENBOT9",
        )

        # Verify starts as 'ready'
        with session_manager.with_meta_session() as session:
            db_env = (
                session.query(RunTimeEnvironment)
                .filter(RunTimeEnvironment.id == env.environment_id)
                .one()
            )
            assert db_env.status == "ready"

        # Start cleanup service
        cleanup_service = EnvironmentCleanupService(
            session_manager=session_manager,
            environment_handler=environment_handler,
            interval_seconds=1,
        )
        await cleanup_service.start()

        # Wait for ONE cycle (should mark as expired)
        await asyncio.sleep(2.5)

        # Verify marked as expired but schema still exists
        with session_manager.with_meta_session() as session:
            db_env = (
                session.query(RunTimeEnvironment)
                .filter(RunTimeEnvironment.id == env.environment_id)
                .one()
            )
            assert db_env.status == "expired"

        assert environment_handler.schema_exists(env.schema_name)

        # Wait for SECOND cycle (should delete)
        await asyncio.sleep(1.5)

        # Stop cleanup service
        await cleanup_service.stop()

        # Now should be deleted
        assert not environment_handler.schema_exists(env.schema_name)

        with session_manager.with_meta_session() as session:
            db_env = (
                session.query(RunTimeEnvironment)
                .filter(RunTimeEnvironment.id == env.environment_id)
                .one()
            )
            assert db_env.status == "deleted"
