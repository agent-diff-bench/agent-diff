from ariadne.asgi import GraphQL
from src.platform.isolationEngine.core import CoreIsolationEngine
from src.platform.evaluationEngine.core import CoreEvaluationEngine


class LinearGraphQL(GraphQL):
    """
    GraphQL handler for Linear service that uses isolated database sessions.

    This class integrates with the platform's IsolationMiddleware which:
    - Authenticates requests via API key
    - Extracts environment_id from URL path
    - Provides scoped database session for the environment
    """

    def __init__(
        self,
        schema,
        coreIsolationEngine: CoreIsolationEngine,
        coreEvaluationEngine: CoreEvaluationEngine,
        session_manager=None,
    ):
        self.coreIsolationEngine = coreIsolationEngine
        self.coreEvaluationEngine = coreEvaluationEngine
        self.session_manager = session_manager
        super().__init__(schema, context_value=self._build_context)

    async def _build_context(self, request, data=None):
        """
        Extract context from request for GraphQL resolvers.

        Extracts environment_id from URL path and creates a session for it.
        This works around Starlette Mount isolation issues.

        Args:
            request: Starlette Request object
            data: GraphQL request data (for Ariadne 0.20+)
        """
        import logging
        logger = logging.getLogger(__name__)

        # Extract env_id from path: /api/env/{env_id}/services/linear/graphql
        path = request.url.path
        logger.info(f"LinearGraphQL._build_context called for path: {path}")

        if "/api/env/" in path:
            path_parts = path.split("/")
            env_id_index = path_parts.index("env") + 1 if "env" in path_parts else None
            if env_id_index and env_id_index < len(path_parts):
                env_id = path_parts[env_id_index]
                logger.info(f"Extracted env_id: {env_id}")

                # Create session directly using session manager
                if self.session_manager:
                    session = self.session_manager.get_session_for_environment(env_id)
                    logger.info(f"Created session: {session}")
                    return {
                        "request": request,
                        "session": session,
                        "environment_id": env_id,
                        "user_id": None,  # Could extract from middleware if needed
                        "impersonate_email": None,
                    }

        logger.error("Failed to create context - missing environment identifier or session manager")
        raise PermissionError("missing environment identifier or session manager")

    async def handle_request(self, request):
        return await super().handle_request(request)
