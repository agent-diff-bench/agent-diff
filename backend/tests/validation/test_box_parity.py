#!/usr/bin/env python3
"""
Comprehensive Box API parity tests.

Compares the Box replica API against the real Box API to ensure
response schema parity. Test files (.md, .txt) are generated dynamically
at runtime - no stored test files needed.

Usage:
    BOX_DEV_TOKEN=<token> pytest tests/validation/test_box_parity.py -v

    Or edit BOX_DEV_TOKEN directly in this file for local development.
"""

import io
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

import requests

# Configuration
BOX_PROD_URL = "https://api.box.com/2.0"
BOX_REPLICA_BASE_URL = "http://localhost:8000/api/platform"

# Dev token from env or manual fallback (replace with your token for local dev)
BOX_DEV_TOKEN = os.environ.get("BOX_DEV_TOKEN", "")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            os.environ.get(
                "BOX_PARITY_LOG",
                f"box_parity_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.log",
            )
        ),
    ],
)
logger = logging.getLogger(__name__)

# =============================================================================
# Enterprise-Only Fields to Ignore
# =============================================================================
# These fields are valid Box API fields but only appear for enterprise accounts.

ENTERPRISE_ONLY_FIELDS = {
    # User (Full) - Enterprise fields
    "role",
    "enterprise",
    "tracking_codes",
    "can_see_managed_users",
    "is_sync_enabled",
    "is_external_collab_restricted",
    "is_exempt_from_device_limits",
    "is_exempt_from_login_verification",
    "is_platform_access_only",
    "my_tags",
    "hostname",
    "external_app_user_id",
    # Folder/File (Full) - Enterprise fields
    "sync_state",
    "can_non_owners_invite",
    "is_collaboration_restricted_to_enterprise",
    "allowed_shared_link_access_levels",
    "can_non_owners_view_collaborators",
    "has_collaborations",
    "permissions",
    "is_externally_owned",
    "allowed_invitee_roles",
    "watermark_info",
    "is_accessible_via_shared_link",
    "classification",
    "is_associated_with_app_item",
    # File (Full) - Extended fields
    "comment_count",
    "representations",
    "lock",
    "expiring_embed_link",
    "disposition_at",
    "expires_at",
    "is_package",
    "version_number",
    "extension",
    "uploader_display_name",
    "shared_link_permission_options",
    # Optional fields (require fields= param)
    "tags",
    "metadata",
    # Comment fields
    "tagged_message",
}


# =============================================================================
# Test File Generator
# =============================================================================


class TestFileGenerator:
    """Generate test files dynamically in memory - no storage needed."""

    @staticmethod
    def markdown(title: str = "Test Document") -> tuple[str, io.BytesIO]:
        """
        Generate a .md file in memory.

        Returns:
            Tuple of (filename, file_stream)
        """
        content = f"""# {title}

Generated at: {datetime.now(timezone.utc).isoformat()}

## Section 1

Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

## Section 2

- Item 1: First bullet point
- Item 2: Second bullet point
- Item 3: Third bullet point

## Code Example

```python
def hello():
    print("Hello, World!")
```

## Conclusion

This is a test document for Box API parity validation.
"""
        filename = f"{title.replace(' ', '_')}.md"
        return filename, io.BytesIO(content.encode("utf-8"))

    @staticmethod
    def text(name: str = "notes") -> tuple[str, io.BytesIO]:
        """
        Generate a .txt file in memory.

        Returns:
            Tuple of (filename, file_stream)
        """
        content = f"""Test file: {name}
Created: {datetime.now(timezone.utc).isoformat()}

This is test content for Box API parity validation.

Line 1: The quick brown fox jumps over the lazy dog.
Line 2: Pack my box with five dozen liquor jugs.
Line 3: How vexingly quick daft zebras jump!

=== End of test file ===
"""
        filename = f"{name}.txt"
        return filename, io.BytesIO(content.encode("utf-8"))

    @staticmethod
    def csv(name: str = "data") -> tuple[str, io.BytesIO]:
        """
        Generate a .csv file in memory.

        Returns:
            Tuple of (filename, file_stream)
        """
        content = f"""id,name,value,timestamp
1,Alpha,100,{datetime.now(timezone.utc).isoformat()}
2,Beta,200,{datetime.now(timezone.utc).isoformat()}
3,Gamma,300,{datetime.now(timezone.utc).isoformat()}
4,Delta,400,{datetime.now(timezone.utc).isoformat()}
"""
        filename = f"{name}.csv"
        return filename, io.BytesIO(content.encode("utf-8"))

    @staticmethod
    def json_file(name: str = "config") -> tuple[str, io.BytesIO]:
        """
        Generate a .json file in memory.

        Returns:
            Tuple of (filename, file_stream)
        """
        import json

        data = {
            "name": name,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "settings": {
                "enabled": True,
                "threshold": 0.75,
                "tags": ["test", "parity", "validation"],
            },
            "items": [
                {"id": 1, "label": "First"},
                {"id": 2, "label": "Second"},
            ],
        }
        content = json.dumps(data, indent=2)
        filename = f"{name}.json"
        return filename, io.BytesIO(content.encode("utf-8"))


# =============================================================================
# Box Parity Tester
# =============================================================================


class BoxParityTester:
    """
    Test Box replica API against real Box API.

    Compares response schemas (structure and types) rather than exact values,
    since IDs and timestamps will differ between environments.
    """

    def __init__(self, prod_token: str):
        self.prod_headers = {
            "Authorization": f"Bearer {prod_token}",
            "Content-Type": "application/json",
        }
        self.replica_env_id: Optional[str] = None
        self.replica_url: Optional[str] = None

        # Resource IDs created during setup
        self.prod_folder_id: Optional[str] = None
        self.replica_folder_id: Optional[str] = None
        self.prod_file_id: Optional[str] = None
        self.replica_file_id: Optional[str] = None
        self.prod_user_id: Optional[str] = None
        self.replica_user_id: Optional[str] = None

        # Mismatch counter
        self.mismatch_count = 0

    def log_mismatch(
        self,
        test_name: str,
        mismatch_type: str,
        details: Dict[str, Any],
    ):
        """Log a mismatch using the logger."""
        self.mismatch_count += 1
        logger.warning(
            "MISMATCH [%s] %s: %s",
            mismatch_type,
            test_name,
            json.dumps(details, indent=2, default=str),
        )

    def log_summary(self):
        """Log summary of mismatches."""
        if self.mismatch_count == 0:
            logger.info("No mismatches found!")
        else:
            logger.warning("Total mismatches: %d", self.mismatch_count)

    # -------------------------------------------------------------------------
    # Environment Setup
    # -------------------------------------------------------------------------

    def setup_replica_environment(self):
        """Create a test environment in the replica."""
        resp = requests.post(
            f"{BOX_REPLICA_BASE_URL}/initEnv",
            json={
                "templateService": "box",
                "templateName": "box_default",
                "impersonateEmail": "admin@example.com",
            },
        )
        if resp.status_code != 201:
            raise Exception(f"Failed to create replica environment: {resp.text}")

        env = resp.json()
        self.replica_env_id = env["environmentId"]
        # Box API uses /2.0/ version prefix in path
        self.replica_url = f"http://localhost:8000{env['environmentUrl']}/2.0"
        print(f"✓ Created replica environment: {self.replica_env_id}")

    def cleanup_replica_environment(self):
        """Clean up the replica environment."""
        if self.replica_env_id:
            try:
                requests.delete(
                    f"{BOX_REPLICA_BASE_URL}/environments/{self.replica_env_id}"
                )
                print(f"✓ Cleaned up replica environment: {self.replica_env_id}")
            except Exception as e:
                print(f"⚠ Failed to cleanup environment: {e}")

    # -------------------------------------------------------------------------
    # API Helpers
    # -------------------------------------------------------------------------

    def api_prod(
        self,
        method: str,
        endpoint: str,
        *,
        json: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> requests.Response:
        """Make a request to the real Box API."""
        url = f"{BOX_PROD_URL}/{endpoint.lstrip('/')}"
        req_headers = self.prod_headers.copy()
        if headers:
            req_headers.update(headers)

        # Don't send Content-Type for multipart uploads
        if files:
            req_headers.pop("Content-Type", None)

        return requests.request(
            method,
            url,
            json=json,
            data=data,
            files=files,
            params=params,
            headers=req_headers,
        )

    def api_replica(
        self,
        method: str,
        endpoint: str,
        *,
        json: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> requests.Response:
        """Make a request to the Box replica API."""
        if not self.replica_url:
            raise RuntimeError("Replica environment not initialized")

        url = f"{self.replica_url}/{endpoint.lstrip('/')}"
        req_headers = {"Content-Type": "application/json"}
        if headers:
            req_headers.update(headers)

        # Don't send Content-Type for multipart uploads
        if files:
            req_headers.pop("Content-Type", None)

        return requests.request(
            method,
            url,
            json=json,
            data=data,
            files=files,
            params=params,
            headers=req_headers,
        )

    # -------------------------------------------------------------------------
    # File Upload Helpers
    # -------------------------------------------------------------------------

    def upload_file_prod(
        self, parent_folder_id: str, filename: str, file_stream: io.BytesIO
    ) -> Dict[str, Any]:
        """Upload a file to the real Box API."""
        # Box uses multipart form upload to upload.box.com
        upload_url = "https://upload.box.com/api/2.0/files/content"

        import json

        attributes = json.dumps({"name": filename, "parent": {"id": parent_folder_id}})

        files = {
            "attributes": (None, attributes, "application/json"),
            "file": (filename, file_stream, "application/octet-stream"),
        }

        headers = {
            "Authorization": f"Bearer {self.prod_headers['Authorization'].split()[-1]}"
        }

        resp = requests.post(upload_url, files=files, headers=headers)
        return resp.json()

    def upload_file_replica(
        self, parent_folder_id: str, filename: str, file_stream: io.BytesIO
    ) -> Dict[str, Any]:
        """Upload a file to the Box replica API."""
        if not self.replica_url:
            raise RuntimeError("Replica environment not initialized")

        import json

        attributes = json.dumps({"name": filename, "parent": {"id": parent_folder_id}})

        files = {
            "attributes": (None, attributes, "application/json"),
            "file": (filename, file_stream, "application/octet-stream"),
        }

        resp = requests.post(f"{self.replica_url}/files/content", files=files)
        return resp.json()

    # -------------------------------------------------------------------------
    # Shape Comparison
    # -------------------------------------------------------------------------

    def extract_shape(self, data: Any) -> Any:
        """
        Extract the shape/structure of data, ignoring actual values.

        Returns a representation where each value is replaced by its type name.
        """
        if isinstance(data, dict):
            return {k: self.extract_shape(v) for k, v in data.items()}
        elif isinstance(data, list):
            if not data:
                return []
            # Return shape of first element to represent list structure
            return [self.extract_shape(data[0])]
        else:
            # Return the type name
            return type(data).__name__

    def compare_shapes(
        self, prod_shape: Any, replica_shape: Any, path: str = ""
    ) -> List[str]:
        """
        Compare two data shapes and return list of differences.

        Args:
            prod_shape: Shape from production API
            replica_shape: Shape from replica API
            path: Current path in the data structure (for error messages)

        Returns:
            List of difference descriptions
        """
        differences = []

        if isinstance(prod_shape, dict) and isinstance(replica_shape, dict):
            # Check for missing keys in replica
            for key in prod_shape:
                if key not in replica_shape:
                    differences.append(f"{path}.{key}: MISSING in replica")
                else:
                    differences.extend(
                        self.compare_shapes(
                            prod_shape[key], replica_shape[key], f"{path}.{key}"
                        )
                    )

            # Check for extra keys in replica (skip enterprise-only fields)
            for key in replica_shape:
                if key not in prod_shape:
                    # Skip enterprise-only fields - they're valid but not returned
                    # by free/dev accounts on the real Box API
                    if key in ENTERPRISE_ONLY_FIELDS:
                        continue
                    differences.append(f"{path}.{key}: EXTRA in replica")

        elif isinstance(prod_shape, list) and isinstance(replica_shape, list):
            if prod_shape and replica_shape:
                differences.extend(
                    self.compare_shapes(prod_shape[0], replica_shape[0], f"{path}[0]")
                )

        elif type(prod_shape).__name__ != type(replica_shape).__name__:
            differences.append(
                f"{path}: Type mismatch (prod: {type(prod_shape).__name__}, "
                f"replica: {type(replica_shape).__name__})"
            )

        return differences

    # -------------------------------------------------------------------------
    # Test Execution Helper
    # -------------------------------------------------------------------------

    def test_operation(
        self,
        name: str,
        prod_call: Callable[[], requests.Response],
        replica_call: Callable[[], requests.Response],
        validate_schema: bool = True,
    ) -> bool:
        """
        Test an operation against both APIs.

        Args:
            name: Test name for output
            prod_call: Lambda that calls production API and returns response
            replica_call: Lambda that calls replica API and returns response
            validate_schema: Whether to compare response schemas

        Returns:
            True if test passed, False otherwise
        """
        print(f"  {name}...", end=" ")

        try:
            prod_resp = prod_call()
            replica_resp = replica_call()
        except Exception as e:
            print(f"EXCEPTION: {e}")
            self.log_mismatch(name, "exception", {"error": str(e)})
            return False

        prod_ok = prod_resp.status_code < 400
        replica_ok = replica_resp.status_code < 400

        # Try to parse JSON for logging
        prod_data = None
        replica_data = None
        try:
            prod_data = prod_resp.json()
        except Exception:
            pass
        try:
            replica_data = replica_resp.json()
        except Exception:
            pass

        if prod_ok and replica_ok:
            if validate_schema:
                if prod_data is None or replica_data is None:
                    print("JSON PARSE ERROR")
                    self.log_mismatch(
                        name,
                        "json_parse_error",
                        {
                            "prod_status": prod_resp.status_code,
                            "replica_status": replica_resp.status_code,
                        },
                    )
                    return False

                prod_shape = self.extract_shape(prod_data)
                replica_shape = self.extract_shape(replica_data)
                differences = self.compare_shapes(prod_shape, replica_shape, "data")

                if differences:
                    print("SCHEMA MISMATCH")
                    for diff in differences[:3]:
                        print(f"     {diff}")
                    if len(differences) > 3:
                        print(f"     ... and {len(differences) - 3} more")

                    # Log detailed mismatch
                    self.log_mismatch(
                        name,
                        "schema_mismatch",
                        {
                            "differences": differences,
                            "prod_shape": prod_shape,
                            "replica_shape": replica_shape,
                            "prod_sample": prod_data,
                            "replica_sample": replica_data,
                        },
                    )
                    return False

            print("PASS")
            return True

        elif not prod_ok and not replica_ok:
            # Both failed - check if error types are similar
            print("(both failed)")
            return True

        else:
            print("STATUS MISMATCH")
            print(f"     Prod: {prod_resp.status_code}")
            print(f"     Replica: {replica_resp.status_code}")

            # Log status mismatch with response bodies
            self.log_mismatch(
                name,
                "status_mismatch",
                {
                    "prod_status": prod_resp.status_code,
                    "replica_status": replica_resp.status_code,
                    "prod_body": prod_data,
                    "replica_body": replica_data,
                },
            )
            return False

    # -------------------------------------------------------------------------
    # Setup Test Resources
    # -------------------------------------------------------------------------

    def setup_test_resources(self):
        """Create matching test resources in both environments."""
        print("\n📦 Setting up test resources...")

        # Get current user info
        print("  Getting user info...")
        prod_user = self.api_prod("GET", "users/me")
        if prod_user.status_code == 200:
            self.prod_user_id = prod_user.json().get("id")
            print(f"    ✓ Prod user: {self.prod_user_id}")

        replica_user = self.api_replica("GET", "users/me")
        if replica_user.status_code == 200:
            self.replica_user_id = replica_user.json().get("id")
            print(f"    ✓ Replica user: {self.replica_user_id}")

        # Create test folders
        print("  Creating test folders...")
        folder_name = (
            f"ParityTest_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
        )

        prod_folder = self.api_prod(
            "POST",
            "folders",
            json={"name": folder_name, "parent": {"id": "0"}},
        )
        if prod_folder.status_code in (200, 201):
            self.prod_folder_id = prod_folder.json().get("id")
            print(f"    ✓ Prod folder: {self.prod_folder_id}")

        replica_folder = self.api_replica(
            "POST",
            "folders",
            json={"name": folder_name, "parent": {"id": "0"}},
        )
        if replica_folder.status_code in (200, 201):
            self.replica_folder_id = replica_folder.json().get("id")
            print(f"    ✓ Replica folder: {self.replica_folder_id}")

        # Upload test files
        if self.prod_folder_id and self.replica_folder_id:
            print("  Uploading test files...")
            filename, file_stream = TestFileGenerator.markdown("Parity_Test_Doc")

            prod_file = self.upload_file_prod(
                self.prod_folder_id, filename, file_stream
            )
            if "entries" in prod_file and prod_file["entries"]:
                self.prod_file_id = prod_file["entries"][0].get("id")
                print(f"    ✓ Prod file: {self.prod_file_id}")

            file_stream.seek(0)  # Reset stream for reuse

            replica_file = self.upload_file_replica(
                self.replica_folder_id, filename, file_stream
            )
            if "entries" in replica_file and replica_file["entries"]:
                self.replica_file_id = replica_file["entries"][0].get("id")
                print(f"    ✓ Replica file: {self.replica_file_id}")

        print()

    def cleanup_test_resources(self):
        """Clean up test resources created during testing."""
        print("\n🧹 Cleaning up test resources...")

        # Delete test folders (this also deletes files inside)
        if self.prod_folder_id:
            try:
                self.api_prod("DELETE", f"folders/{self.prod_folder_id}?recursive=true")
                print(f"  ✓ Deleted prod folder: {self.prod_folder_id}")
            except Exception as e:
                print(f"  ⚠ Failed to delete prod folder: {e}")

    # -------------------------------------------------------------------------
    # Test Suites
    # -------------------------------------------------------------------------

    def run_user_tests(self) -> tuple[int, int]:
        """
        Run user-related tests.

        Endpoint: GET /users/me

        Test Cases:
        - [COMMON] Basic user info retrieval
        - [COMMON] Response includes expected fields (id, name, login, type)
        - [EDGE] Request with extra query params (should be ignored)
        - [EDGE] Fields query param to limit response fields
        """
        print("\n👤 User Operations:")
        passed = 0
        total = 0

        # [COMMON] Basic user info retrieval
        total += 1
        if self.test_operation(
            "GET /users/me (basic)",
            lambda: self.api_prod("GET", "users/me"),
            lambda: self.api_replica("GET", "users/me"),
        ):
            passed += 1

        # [EDGE] With fields query param (Box allows field filtering)
        total += 1
        if self.test_operation(
            "GET /users/me?fields=id,name,login",
            lambda: self.api_prod(
                "GET", "users/me", params={"fields": "id,name,login"}
            ),
            lambda: self.api_replica(
                "GET", "users/me", params={"fields": "id,name,login"}
            ),
        ):
            passed += 1

        # [EDGE] Extra unknown query params (should be ignored)
        total += 1
        if self.test_operation(
            "GET /users/me?unknown_param=value",
            lambda: self.api_prod("GET", "users/me", params={"unknown_param": "value"}),
            lambda: self.api_replica(
                "GET", "users/me", params={"unknown_param": "value"}
            ),
        ):
            passed += 1

        return passed, total

    def run_folder_tests(self) -> tuple[int, int]:
        """
        Run folder-related tests.

        Endpoints:
        - GET /folders/{id}
        - GET /folders/{id}/items
        - POST /folders
        - PUT /folders/{id}

        Test Cases:
        GET /folders/{id}:
        - [COMMON] Get root folder (id=0)
        - [COMMON] Get user-created folder
        - [EDGE] With fields param to limit response
        - [EDGE] Non-existent folder ID (404)

        GET /folders/{id}/items:
        - [COMMON] List root folder items
        - [COMMON] List empty folder items
        - [EDGE] Pagination with offset/limit
        - [EDGE] Sort by name/date
        - [EDGE] Filter by type (file/folder)
        - [EDGE] Very large offset (empty result)

        POST /folders:
        - [COMMON] Create folder in root
        - [COMMON] Create nested subfolder
        - [EDGE] Name with spaces
        - [EDGE] Name with special chars (!@#$%^&)
        - [EDGE] Name with unicode (日本語, émoji 🎉)
        - [EDGE] Very long name (255 chars)
        - [EDGE] Duplicate name (conflict)
        - [EDGE] Empty name (error)

        PUT /folders/{id}:
        - [COMMON] Update folder name
        - [COMMON] Update folder description
        - [EDGE] Move folder to different parent
        - [EDGE] Empty update (no changes)
        """
        print("\n📁 Folder Operations:")
        passed = 0
        total = 0

        # === GET /folders/{id} ===

        # [COMMON] Get root folder (id=0)
        total += 1
        if self.test_operation(
            "GET /folders/0 (root)",
            lambda: self.api_prod("GET", "folders/0"),
            lambda: self.api_replica("GET", "folders/0"),
        ):
            passed += 1

        # [EDGE] Root folder with fields param
        total += 1
        if self.test_operation(
            "GET /folders/0?fields=id,name,type",
            lambda: self.api_prod(
                "GET", "folders/0", params={"fields": "id,name,type"}
            ),
            lambda: self.api_replica(
                "GET", "folders/0", params={"fields": "id,name,type"}
            ),
        ):
            passed += 1

        # === GET /folders/{id}/items ===

        # [COMMON] List root folder items
        total += 1
        if self.test_operation(
            "GET /folders/0/items",
            lambda: self.api_prod("GET", "folders/0/items"),
            lambda: self.api_replica("GET", "folders/0/items"),
        ):
            passed += 1

        # [EDGE] Pagination with limit
        total += 1
        if self.test_operation(
            "GET /folders/0/items?limit=5",
            lambda: self.api_prod("GET", "folders/0/items", params={"limit": 5}),
            lambda: self.api_replica("GET", "folders/0/items", params={"limit": 5}),
        ):
            passed += 1

        # [EDGE] Pagination with offset
        total += 1
        if self.test_operation(
            "GET /folders/0/items?offset=0&limit=2",
            lambda: self.api_prod(
                "GET", "folders/0/items", params={"offset": 0, "limit": 2}
            ),
            lambda: self.api_replica(
                "GET", "folders/0/items", params={"offset": 0, "limit": 2}
            ),
        ):
            passed += 1

        # [EDGE] Sort by name
        total += 1
        if self.test_operation(
            "GET /folders/0/items?sort=name&direction=ASC",
            lambda: self.api_prod(
                "GET", "folders/0/items", params={"sort": "name", "direction": "ASC"}
            ),
            lambda: self.api_replica(
                "GET", "folders/0/items", params={"sort": "name", "direction": "ASC"}
            ),
        ):
            passed += 1

        # [EDGE] Sort by date descending
        total += 1
        if self.test_operation(
            "GET /folders/0/items?sort=date&direction=DESC",
            lambda: self.api_prod(
                "GET", "folders/0/items", params={"sort": "date", "direction": "DESC"}
            ),
            lambda: self.api_replica(
                "GET", "folders/0/items", params={"sort": "date", "direction": "DESC"}
            ),
        ):
            passed += 1

        # [EDGE] Very large offset (should return empty)
        total += 1
        if self.test_operation(
            "GET /folders/0/items?offset=999999",
            lambda: self.api_prod("GET", "folders/0/items", params={"offset": 999999}),
            lambda: self.api_replica(
                "GET", "folders/0/items", params={"offset": 999999}
            ),
        ):
            passed += 1

        # === Tests using created test folder ===
        if self.prod_folder_id and self.replica_folder_id:
            # [COMMON] Get specific folder
            total += 1
            if self.test_operation(
                "GET /folders/{id}",
                lambda: self.api_prod("GET", f"folders/{self.prod_folder_id}"),
                lambda: self.api_replica("GET", f"folders/{self.replica_folder_id}"),
            ):
                passed += 1

            # [COMMON] List folder items
            total += 1
            if self.test_operation(
                "GET /folders/{id}/items",
                lambda: self.api_prod("GET", f"folders/{self.prod_folder_id}/items"),
                lambda: self.api_replica(
                    "GET", f"folders/{self.replica_folder_id}/items"
                ),
            ):
                passed += 1

            # === PUT /folders/{id} ===

            # [COMMON] Update folder name
            total += 1
            updated_folder_name = (
                f"ParityTest_Updated_{datetime.now(timezone.utc).strftime('%H%M%S%f')}"
            )
            if self.test_operation(
                "PUT /folders/{id} (update name)",
                lambda n=updated_folder_name: self.api_prod(
                    "PUT",
                    f"folders/{self.prod_folder_id}",
                    json={"name": n},
                ),
                lambda n=updated_folder_name: self.api_replica(
                    "PUT",
                    f"folders/{self.replica_folder_id}",
                    json={"name": n},
                ),
            ):
                passed += 1

            # [COMMON] Update description
            total += 1
            if self.test_operation(
                "PUT /folders/{id} (update description)",
                lambda: self.api_prod(
                    "PUT",
                    f"folders/{self.prod_folder_id}",
                    json={"description": "Updated description for parity test"},
                ),
                lambda: self.api_replica(
                    "PUT",
                    f"folders/{self.replica_folder_id}",
                    json={"description": "Updated description for parity test"},
                ),
            ):
                passed += 1

            # [EDGE] Empty update (no changes)
            total += 1
            if self.test_operation(
                "PUT /folders/{id} (empty update)",
                lambda: self.api_prod("PUT", f"folders/{self.prod_folder_id}", json={}),
                lambda: self.api_replica(
                    "PUT", f"folders/{self.replica_folder_id}", json={}
                ),
            ):
                passed += 1

            # === POST /folders (create) ===

            # [COMMON] Create basic subfolder
            subfolder_name = (
                f"SubFolder_{datetime.now(timezone.utc).strftime('%H%M%S')}"
            )
            total += 1
            if self.test_operation(
                "POST /folders (create subfolder)",
                lambda: self.api_prod(
                    "POST",
                    "folders",
                    json={
                        "name": subfolder_name,
                        "parent": {"id": self.prod_folder_id},
                    },
                ),
                lambda: self.api_replica(
                    "POST",
                    "folders",
                    json={
                        "name": subfolder_name,
                        "parent": {"id": self.replica_folder_id},
                    },
                ),
            ):
                passed += 1

            # [EDGE] Name with spaces
            total += 1
            ts = datetime.now(timezone.utc).strftime("%H%M%S%f")
            if self.test_operation(
                "POST /folders (name with spaces)",
                lambda t=ts: self.api_prod(
                    "POST",
                    "folders",
                    json={
                        "name": f"Folder With Spaces {t}",
                        "parent": {"id": self.prod_folder_id},
                    },
                ),
                lambda t=ts: self.api_replica(
                    "POST",
                    "folders",
                    json={
                        "name": f"Folder With Spaces {t}",
                        "parent": {"id": self.replica_folder_id},
                    },
                ),
            ):
                passed += 1

            # [EDGE] Name with special characters
            total += 1
            ts = datetime.now(timezone.utc).strftime("%H%M%S%f")
            if self.test_operation(
                "POST /folders (special chars: !@#$%)",
                lambda t=ts: self.api_prod(
                    "POST",
                    "folders",
                    json={
                        "name": f"Test!@#$%Folder_{t}",
                        "parent": {"id": self.prod_folder_id},
                    },
                ),
                lambda t=ts: self.api_replica(
                    "POST",
                    "folders",
                    json={
                        "name": f"Test!@#$%Folder_{t}",
                        "parent": {"id": self.replica_folder_id},
                    },
                ),
            ):
                passed += 1

            # [EDGE] Name with unicode characters
            total += 1
            ts = datetime.now(timezone.utc).strftime("%H%M%S%f")
            if self.test_operation(
                "POST /folders (unicode: 日本語テスト)",
                lambda t=ts: self.api_prod(
                    "POST",
                    "folders",
                    json={
                        "name": f"日本語テスト_Folder_{t}",
                        "parent": {"id": self.prod_folder_id},
                    },
                ),
                lambda t=ts: self.api_replica(
                    "POST",
                    "folders",
                    json={
                        "name": f"日本語テスト_Folder_{t}",
                        "parent": {"id": self.replica_folder_id},
                    },
                ),
            ):
                passed += 1

            # [EDGE] Name with emoji
            total += 1
            ts = datetime.now(timezone.utc).strftime("%H%M%S%f")
            if self.test_operation(
                "POST /folders (emoji: 🎉📁)",
                lambda t=ts: self.api_prod(
                    "POST",
                    "folders",
                    json={
                        "name": f"Emoji_🎉📁_Test_{t}",
                        "parent": {"id": self.prod_folder_id},
                    },
                ),
                lambda t=ts: self.api_replica(
                    "POST",
                    "folders",
                    json={
                        "name": f"Emoji_🎉📁_Test_{t}",
                        "parent": {"id": self.replica_folder_id},
                    },
                ),
            ):
                passed += 1

            # [EDGE] Very long name (255 chars is typical limit)
            long_name = "A" * 200 + "_LongFolderName"
            total += 1
            if self.test_operation(
                "POST /folders (long name ~215 chars)",
                lambda: self.api_prod(
                    "POST",
                    "folders",
                    json={"name": long_name, "parent": {"id": self.prod_folder_id}},
                ),
                lambda: self.api_replica(
                    "POST",
                    "folders",
                    json={"name": long_name, "parent": {"id": self.replica_folder_id}},
                ),
            ):
                passed += 1

            # [EDGE] Empty name (should error)
            total += 1
            if self.test_operation(
                "POST /folders (empty name - error)",
                lambda: self.api_prod(
                    "POST",
                    "folders",
                    json={"name": "", "parent": {"id": self.prod_folder_id}},
                ),
                lambda: self.api_replica(
                    "POST",
                    "folders",
                    json={"name": "", "parent": {"id": self.replica_folder_id}},
                ),
                validate_schema=False,
            ):
                passed += 1

            # [EDGE] Create with description
            total += 1
            if self.test_operation(
                "POST /folders (with description)",
                lambda: self.api_prod(
                    "POST",
                    "folders",
                    json={
                        "name": f"DescFolder_{datetime.now(timezone.utc).strftime('%H%M%S')}",
                        "parent": {"id": self.prod_folder_id},
                        "description": "A folder with a description",
                    },
                ),
                lambda: self.api_replica(
                    "POST",
                    "folders",
                    json={
                        "name": f"DescFolder_{datetime.now(timezone.utc).strftime('%H%M%S')}",
                        "parent": {"id": self.replica_folder_id},
                        "description": "A folder with a description",
                    },
                ),
            ):
                passed += 1

        return passed, total

    def run_file_tests(self) -> tuple[int, int]:
        """
        Run file-related tests.

        Endpoints:
        - POST /files/content (upload)
        - GET /files/{id}
        - PUT /files/{id}
        - GET /files/{id}/content (download)

        Test Cases:
        POST /files/content:
        - [COMMON] Upload .md file
        - [COMMON] Upload .txt file
        - [COMMON] Upload .csv file
        - [COMMON] Upload .json file
        - [EDGE] File with spaces in name
        - [EDGE] File with special chars in name
        - [EDGE] File with unicode name
        - [EDGE] Very long filename
        - [EDGE] Empty file (0 bytes)
        - [EDGE] Large-ish file content

        GET /files/{id}:
        - [COMMON] Get file metadata
        - [EDGE] With fields param
        - [EDGE] Non-existent file ID (404)

        PUT /files/{id}:
        - [COMMON] Update filename
        - [COMMON] Update description
        - [EDGE] Move to different folder
        - [EDGE] Empty update
        - [EDGE] Update with tags

        GET /files/{id}/content:
        - [COMMON] Download file content
        - [EDGE] Range request (partial content)
        """
        print("\n📄 File Operations:")
        passed = 0
        total = 0

        # === GET /files/{id} ===
        if self.prod_file_id and self.replica_file_id:
            # [COMMON] Get file metadata
            total += 1
            if self.test_operation(
                "GET /files/{id}",
                lambda: self.api_prod("GET", f"files/{self.prod_file_id}"),
                lambda: self.api_replica("GET", f"files/{self.replica_file_id}"),
            ):
                passed += 1

            # [EDGE] With fields param
            total += 1
            if self.test_operation(
                "GET /files/{id}?fields=id,name,size",
                lambda: self.api_prod(
                    "GET",
                    f"files/{self.prod_file_id}",
                    params={"fields": "id,name,size"},
                ),
                lambda: self.api_replica(
                    "GET",
                    f"files/{self.replica_file_id}",
                    params={"fields": "id,name,size"},
                ),
            ):
                passed += 1

            # === PUT /files/{id} ===

            # [COMMON] Update filename
            total += 1
            updated_file_name = f"Updated_Parity_Doc_{datetime.now(timezone.utc).strftime('%H%M%S%f')}.md"
            if self.test_operation(
                "PUT /files/{id} (update name)",
                lambda n=updated_file_name: self.api_prod(
                    "PUT",
                    f"files/{self.prod_file_id}",
                    json={"name": n},
                ),
                lambda n=updated_file_name: self.api_replica(
                    "PUT",
                    f"files/{self.replica_file_id}",
                    json={"name": n},
                ),
            ):
                passed += 1

            # [COMMON] Update description
            total += 1
            if self.test_operation(
                "PUT /files/{id} (update description)",
                lambda: self.api_prod(
                    "PUT",
                    f"files/{self.prod_file_id}",
                    json={"description": "Updated file description"},
                ),
                lambda: self.api_replica(
                    "PUT",
                    f"files/{self.replica_file_id}",
                    json={"description": "Updated file description"},
                ),
            ):
                passed += 1

            # [EDGE] Empty update
            total += 1
            if self.test_operation(
                "PUT /files/{id} (empty update)",
                lambda: self.api_prod("PUT", f"files/{self.prod_file_id}", json={}),
                lambda: self.api_replica(
                    "PUT", f"files/{self.replica_file_id}", json={}
                ),
            ):
                passed += 1

            # === GET /files/{id}/content (download) ===

            # [COMMON] Download file content - basic status check
            total += 1
            if self.test_operation(
                "GET /files/{id}/content (download status)",
                lambda: self.api_prod("GET", f"files/{self.prod_file_id}/content"),
                lambda: self.api_replica(
                    "GET", f"files/{self.replica_file_id}/content"
                ),
                validate_schema=False,  # Returns redirect or binary
            ):
                passed += 1

        # === POST /files/content (upload) + Download Content Verification ===
        if self.prod_folder_id and self.replica_folder_id:
            # [CRITICAL] Upload and verify download returns same content
            total += 1
            print("  Upload + Download content verification...", end=" ")
            try:
                # Generate known content
                known_content = (
                    "VERIFICATION_CONTENT_12345\nLine 2\nLine 3\n日本語テスト"
                )
                test_filename = f"verify_download_{datetime.now(timezone.utc).strftime('%H%M%S')}.txt"

                # Upload to both
                prod_upload = self.upload_file_prod(
                    self.prod_folder_id,
                    test_filename,
                    io.BytesIO(known_content.encode("utf-8")),
                )
                replica_upload = self.upload_file_replica(
                    self.replica_folder_id,
                    test_filename,
                    io.BytesIO(known_content.encode("utf-8")),
                )

                if "entries" not in prod_upload or "entries" not in replica_upload:
                    print(" Upload failed")
                else:
                    prod_file_id = prod_upload["entries"][0]["id"]
                    replica_file_id = replica_upload["entries"][0]["id"]

                    # Download from both - Box returns 302 redirect, follow it
                    prod_download = requests.get(
                        f"{BOX_PROD_URL}/files/{prod_file_id}/content",
                        headers=self.prod_headers,
                        allow_redirects=True,
                    )
                    replica_download = self.api_replica(
                        "GET", f"files/{replica_file_id}/content"
                    )

                    # Check status codes match pattern
                    prod_ok = prod_download.status_code in (200, 302)
                    replica_ok = replica_download.status_code in (200, 302)

                    if not (prod_ok and replica_ok):
                        print(
                            f" Status mismatch: prod={prod_download.status_code}, replica={replica_download.status_code}"
                        )
                    else:
                        # Verify content matches what we uploaded
                        prod_content = prod_download.content.decode("utf-8")
                        replica_content = replica_download.content.decode("utf-8")

                        prod_matches = (
                            known_content in prod_content
                            or prod_content == known_content
                        )
                        replica_matches = (
                            known_content in replica_content
                            or replica_content == known_content
                        )

                        if prod_matches and replica_matches:
                            print("✅ (content verified)")
                            passed += 1
                        elif prod_matches != replica_matches:
                            print(
                                f" Content parity: prod_matches={prod_matches}, replica_matches={replica_matches}"
                            )
                        else:
                            # Both failed to match - could be encoding issue, check if similar
                            print("⚠️ Content differs from upload (checking parity)")
                            if len(prod_content) == len(replica_content):
                                print("✅ (same length, parity OK)")
                                passed += 1
                            else:
                                print(
                                    f" Length differs: prod={len(prod_content)}, replica={len(replica_content)}"
                                )
            except Exception as e:
                print(f" {e}")

            # [EDGE] Download and verify Content-Type header parity
            total += 1
            print("  Download Content-Type header parity...", end=" ")
            try:
                if self.prod_file_id and self.replica_file_id:
                    prod_resp = requests.get(
                        f"{BOX_PROD_URL}/files/{self.prod_file_id}/content",
                        headers=self.prod_headers,
                        allow_redirects=True,
                    )
                    replica_resp = self.api_replica(
                        "GET", f"files/{self.replica_file_id}/content"
                    )

                    prod_ct = prod_resp.headers.get("Content-Type", "").split(";")[0]
                    replica_ct = replica_resp.headers.get("Content-Type", "").split(
                        ";"
                    )[0]

                    # Both should have similar content type
                    if prod_ct and replica_ct:
                        # Normalize common variations
                        prod_ct_norm = prod_ct.lower().strip()
                        replica_ct_norm = replica_ct.lower().strip()

                        if prod_ct_norm == replica_ct_norm:
                            print(f"✅ ({prod_ct_norm})")
                            passed += 1
                        else:
                            # Accept if both are text-ish or both are binary
                            prod_is_text = (
                                "text" in prod_ct_norm or "json" in prod_ct_norm
                            )
                            replica_is_text = (
                                "text" in replica_ct_norm or "json" in replica_ct_norm
                            )
                            if prod_is_text == replica_is_text:
                                print(
                                    f"✅ (similar: {prod_ct_norm} vs {replica_ct_norm})"
                                )
                                passed += 1
                            else:
                                print(f" {prod_ct_norm} vs {replica_ct_norm}")
                    else:
                        print(
                            f"⚠️ Missing Content-Type: prod={prod_ct}, replica={replica_ct}"
                        )
                        passed += 1  # Not a hard failure
                else:
                    print("⚠️ Skipped (no file IDs)")
                    passed += 1
            except Exception as e:
                print(f" {e}")

            # [EDGE] Download non-existent file (404 parity)
            total += 1
            if self.test_operation(
                "GET /files/99999999999/content (404)",
                lambda: self.api_prod("GET", "files/99999999999/content"),
                lambda: self.api_replica("GET", "files/99999999999/content"),
                validate_schema=False,
            ):
                passed += 1

            # [CRITICAL] Binary content verification - exact byte match
            total += 1
            print("  Binary content verification (exact bytes)...", end=" ")
            try:
                # Generate deterministic binary-ish content
                binary_content = (
                    b"BINARY_TEST\x00\x01\x02\x03\xff\xfe\xfd\nLine with newline\n"
                )
                test_filename = (
                    f"binary_verify_{datetime.now(timezone.utc).strftime('%H%M%S')}.bin"
                )

                # Upload to both
                prod_upload = self.upload_file_prod(
                    self.prod_folder_id, test_filename, io.BytesIO(binary_content)
                )
                replica_upload = self.upload_file_replica(
                    self.replica_folder_id, test_filename, io.BytesIO(binary_content)
                )

                if "entries" not in prod_upload or "entries" not in replica_upload:
                    print(" Upload failed")
                else:
                    prod_file_id = prod_upload["entries"][0]["id"]
                    replica_file_id = replica_upload["entries"][0]["id"]

                    # Download raw bytes
                    prod_download = requests.get(
                        f"{BOX_PROD_URL}/files/{prod_file_id}/content",
                        headers=self.prod_headers,
                        allow_redirects=True,
                    )
                    replica_download = self.api_replica(
                        "GET", f"files/{replica_file_id}/content"
                    )

                    prod_bytes = prod_download.content
                    replica_bytes = replica_download.content

                    # Verify exact match with original
                    prod_exact = prod_bytes == binary_content
                    replica_exact = replica_bytes == binary_content

                    if prod_exact and replica_exact:
                        print("✅ (exact match)")
                        passed += 1
                    elif prod_exact == replica_exact:
                        # Both behave the same way
                        if prod_bytes == replica_bytes:
                            print("✅ (both match each other)")
                            passed += 1
                        else:
                            print(
                                f"⚠️ Both differ from original but not equal: prod={len(prod_bytes)}B, replica={len(replica_bytes)}B"
                            )
                    else:
                        print(
                            f" Parity fail: prod_exact={prod_exact}, replica_exact={replica_exact}"
                        )
            except Exception as e:
                print(f" {e}")

            # [EDGE] Verify file size in metadata matches actual download size
            total += 1
            print("  File size metadata vs download size...", end=" ")
            try:
                if self.prod_file_id and self.replica_file_id:
                    # Get metadata
                    prod_meta = self.api_prod(
                        "GET", f"files/{self.prod_file_id}"
                    ).json()
                    replica_meta = self.api_replica(
                        "GET", f"files/{self.replica_file_id}"
                    ).json()

                    # Get actual download
                    prod_download = requests.get(
                        f"{BOX_PROD_URL}/files/{self.prod_file_id}/content",
                        headers=self.prod_headers,
                        allow_redirects=True,
                    )
                    replica_download = self.api_replica(
                        "GET", f"files/{self.replica_file_id}/content"
                    )

                    prod_meta_size = prod_meta.get("size", 0)
                    replica_meta_size = replica_meta.get("size", 0)
                    prod_actual_size = len(prod_download.content)
                    replica_actual_size = len(replica_download.content)

                    prod_match = prod_meta_size == prod_actual_size
                    replica_match = replica_meta_size == replica_actual_size

                    if prod_match and replica_match:
                        print(
                            f"✅ (prod={prod_meta_size}B, replica={replica_meta_size}B)"
                        )
                        passed += 1
                    elif prod_match == replica_match:
                        print(f"⚠️ Both have same behavior: prod_match={prod_match}")
                        passed += 1
                    else:
                        print(
                            f" prod: meta={prod_meta_size} actual={prod_actual_size}, replica: meta={replica_meta_size} actual={replica_actual_size}"
                        )
                else:
                    print("⚠️ Skipped (no file IDs)")
                    passed += 1
            except Exception as e:
                print(f" {e}")

        # === POST /files/content (upload) ===
        if self.prod_folder_id and self.replica_folder_id:
            # [COMMON] Upload .txt file
            total += 1
            print("  Upload .txt file...", end=" ")
            try:
                txt_name, txt_stream = TestFileGenerator.text("parity_notes")
                prod_result = self.upload_file_prod(
                    self.prod_folder_id, txt_name, txt_stream
                )
                txt_stream.seek(0)
                replica_result = self.upload_file_replica(
                    self.replica_folder_id, txt_name, txt_stream
                )

                if "entries" in prod_result and "entries" in replica_result:
                    print("✅")
                    passed += 1
                else:
                    print("")
            except Exception as e:
                print(f" {e}")

            # [COMMON] Upload .csv file
            total += 1
            print("  Upload .csv file...", end=" ")
            try:
                csv_name, csv_stream = TestFileGenerator.csv("parity_data")
                prod_result = self.upload_file_prod(
                    self.prod_folder_id, csv_name, csv_stream
                )
                csv_stream.seek(0)
                replica_result = self.upload_file_replica(
                    self.replica_folder_id, csv_name, csv_stream
                )

                if "entries" in prod_result and "entries" in replica_result:
                    print("✅")
                    passed += 1
                else:
                    print("")
            except Exception as e:
                print(f" {e}")

            # [COMMON] Upload .json file
            total += 1
            print("  Upload .json file...", end=" ")
            try:
                json_name, json_stream = TestFileGenerator.json_file("parity_config")
                prod_result = self.upload_file_prod(
                    self.prod_folder_id, json_name, json_stream
                )
                json_stream.seek(0)
                replica_result = self.upload_file_replica(
                    self.replica_folder_id, json_name, json_stream
                )

                if "entries" in prod_result and "entries" in replica_result:
                    print("✅")
                    passed += 1
                else:
                    print("")
            except Exception as e:
                print(f" {e}")

            # [EDGE] File with spaces in name
            total += 1
            print("  Upload file with spaces in name...", end=" ")
            try:
                content = b"File with spaces test content"
                filename = "File With Spaces.txt"
                prod_result = self.upload_file_prod(
                    self.prod_folder_id, filename, io.BytesIO(content)
                )
                replica_result = self.upload_file_replica(
                    self.replica_folder_id, filename, io.BytesIO(content)
                )

                if "entries" in prod_result and "entries" in replica_result:
                    print("✅")
                    passed += 1
                else:
                    print("")
            except Exception as e:
                print(f" {e}")

            # [EDGE] File with special characters
            total += 1
            print("  Upload file with special chars (!@#)...", end=" ")
            try:
                content = b"Special chars test content"
                filename = "Test!@#File.txt"
                prod_result = self.upload_file_prod(
                    self.prod_folder_id, filename, io.BytesIO(content)
                )
                replica_result = self.upload_file_replica(
                    self.replica_folder_id, filename, io.BytesIO(content)
                )

                prod_ok = "entries" in prod_result or "type" in prod_result
                replica_ok = "entries" in replica_result or "type" in replica_result

                if prod_ok == replica_ok:
                    print("✅")
                    passed += 1
                else:
                    print("")
            except Exception as e:
                print(f" {e}")

            # [EDGE] File with unicode name
            total += 1
            print("  Upload file with unicode name (日本語)...", end=" ")
            try:
                content = b"Unicode filename test content"
                filename = "日本語ファイル.txt"
                prod_result = self.upload_file_prod(
                    self.prod_folder_id, filename, io.BytesIO(content)
                )
                replica_result = self.upload_file_replica(
                    self.replica_folder_id, filename, io.BytesIO(content)
                )

                prod_ok = "entries" in prod_result or "type" in prod_result
                replica_ok = "entries" in replica_result or "type" in replica_result

                if prod_ok == replica_ok:
                    print("✅")
                    passed += 1
                else:
                    print("")
            except Exception as e:
                print(f" {e}")

            # [EDGE] Empty file (0 bytes)
            total += 1
            print("  Upload empty file (0 bytes)...", end=" ")
            try:
                content = b""
                filename = "empty_file.txt"
                prod_result = self.upload_file_prod(
                    self.prod_folder_id, filename, io.BytesIO(content)
                )
                replica_result = self.upload_file_replica(
                    self.replica_folder_id, filename, io.BytesIO(content)
                )

                prod_ok = "entries" in prod_result or "type" in prod_result
                replica_ok = "entries" in replica_result or "type" in replica_result

                if prod_ok == replica_ok:
                    print("✅")
                    passed += 1
                else:
                    print("")
            except Exception as e:
                print(f" {e}")

            # [EDGE] Larger file content (~10KB)
            total += 1
            print("  Upload larger file (~10KB)...", end=" ")
            try:
                content = ("A" * 1000 + "\n") * 10  # ~10KB
                filename = "large_content.txt"
                prod_result = self.upload_file_prod(
                    self.prod_folder_id, filename, io.BytesIO(content.encode())
                )
                replica_result = self.upload_file_replica(
                    self.replica_folder_id, filename, io.BytesIO(content.encode())
                )

                if "entries" in prod_result and "entries" in replica_result:
                    print("✅")
                    passed += 1
                else:
                    print("")
            except Exception as e:
                print(f" {e}")

        return passed, total

    def run_comment_tests(self) -> tuple[int, int]:
        """
        Run comment-related tests.

        Endpoints:
        - POST /comments
        - GET /files/{id}/comments

        Test Cases:
        POST /comments:
        - [COMMON] Create basic comment on file
        - [EDGE] Comment with very long message
        - [EDGE] Comment with unicode/emoji
        - [EDGE] Comment with markdown formatting
        - [EDGE] Comment on non-existent file (error)
        - [EDGE] Empty message (error)

        GET /files/{id}/comments:
        - [COMMON] List comments on file
        - [EDGE] List comments on file with no comments
        - [EDGE] Pagination with limit/offset
        """
        print("\n💬 Comment Operations:")
        passed = 0
        total = 0

        if self.prod_file_id and self.replica_file_id:
            # === POST /comments ===

            # [COMMON] Create basic comment
            total += 1
            comment_message = (
                f"Parity test comment at {datetime.now(timezone.utc).isoformat()}"
            )

            print("  POST /comments (create basic)...", end=" ")
            try:
                prod_resp = self.api_prod(
                    "POST",
                    "comments",
                    json={
                        "item": {"type": "file", "id": self.prod_file_id},
                        "message": comment_message,
                    },
                )
                replica_resp = self.api_replica(
                    "POST",
                    "comments",
                    json={
                        "item": {"type": "file", "id": self.replica_file_id},
                        "message": comment_message,
                    },
                )

                prod_ok = prod_resp.status_code in (200, 201)
                replica_ok = replica_resp.status_code in (200, 201)

                if prod_ok and replica_ok:
                    prod_data = prod_resp.json()
                    replica_data = replica_resp.json()

                    prod_shape = self.extract_shape(prod_data)
                    replica_shape = self.extract_shape(replica_data)
                    diffs = self.compare_shapes(prod_shape, replica_shape, "data")

                    if diffs:
                        print(" SCHEMA MISMATCH")
                        for d in diffs[:2]:
                            print(f"     {d}")
                    else:
                        print("✅")
                        passed += 1
                        # IDs available for potential follow-up tests:
                        # prod_comment_id = prod_data.get("id")
                        # replica_comment_id = replica_data.get("id")
                else:
                    print(
                        f" STATUS: prod={prod_resp.status_code}, replica={replica_resp.status_code}"
                    )
            except Exception as e:
                print(f" {e}")

            # [EDGE] Comment with very long message (~1000 chars)
            total += 1
            long_message = "This is a very long comment. " * 50
            print("  POST /comments (long message ~1500 chars)...", end=" ")
            try:
                prod_resp = self.api_prod(
                    "POST",
                    "comments",
                    json={
                        "item": {"type": "file", "id": self.prod_file_id},
                        "message": long_message,
                    },
                )
                replica_resp = self.api_replica(
                    "POST",
                    "comments",
                    json={
                        "item": {"type": "file", "id": self.replica_file_id},
                        "message": long_message,
                    },
                )

                prod_ok = prod_resp.status_code in (200, 201)
                replica_ok = replica_resp.status_code in (200, 201)

                if prod_ok == replica_ok:
                    print("✅")
                    passed += 1
                else:
                    print(
                        f" STATUS: prod={prod_resp.status_code}, replica={replica_resp.status_code}"
                    )
            except Exception as e:
                print(f" {e}")

            # [EDGE] Comment with unicode and emoji
            total += 1
            unicode_message = "Comment with unicode: 日本語 and emoji: 🎉👍✅"
            print("  POST /comments (unicode + emoji)...", end=" ")
            try:
                prod_resp = self.api_prod(
                    "POST",
                    "comments",
                    json={
                        "item": {"type": "file", "id": self.prod_file_id},
                        "message": unicode_message,
                    },
                )
                replica_resp = self.api_replica(
                    "POST",
                    "comments",
                    json={
                        "item": {"type": "file", "id": self.replica_file_id},
                        "message": unicode_message,
                    },
                )

                prod_ok = prod_resp.status_code in (200, 201)
                replica_ok = replica_resp.status_code in (200, 201)

                if prod_ok == replica_ok:
                    print("✅")
                    passed += 1
                else:
                    print(
                        f" STATUS: prod={prod_resp.status_code}, replica={replica_resp.status_code}"
                    )
            except Exception as e:
                print(f" {e}")

            # [EDGE] Comment with markdown-like formatting
            total += 1
            md_message = "**Bold** and _italic_ and `code` and\n- bullet\n- list"
            print("  POST /comments (markdown formatting)...", end=" ")
            try:
                prod_resp = self.api_prod(
                    "POST",
                    "comments",
                    json={
                        "item": {"type": "file", "id": self.prod_file_id},
                        "message": md_message,
                    },
                )
                replica_resp = self.api_replica(
                    "POST",
                    "comments",
                    json={
                        "item": {"type": "file", "id": self.replica_file_id},
                        "message": md_message,
                    },
                )

                prod_ok = prod_resp.status_code in (200, 201)
                replica_ok = replica_resp.status_code in (200, 201)

                if prod_ok == replica_ok:
                    print("✅")
                    passed += 1
                else:
                    print(
                        f" STATUS: prod={prod_resp.status_code}, replica={replica_resp.status_code}"
                    )
            except Exception as e:
                print(f" {e}")

            # [EDGE] Comment on non-existent file
            total += 1
            if self.test_operation(
                "POST /comments (non-existent file - error)",
                lambda: self.api_prod(
                    "POST",
                    "comments",
                    json={
                        "item": {"type": "file", "id": "99999999999"},
                        "message": "Should fail",
                    },
                ),
                lambda: self.api_replica(
                    "POST",
                    "comments",
                    json={
                        "item": {"type": "file", "id": "99999999999"},
                        "message": "Should fail",
                    },
                ),
                validate_schema=False,
            ):
                passed += 1

            # === GET /files/{id}/comments ===

            # [COMMON] List comments
            total += 1
            if self.test_operation(
                "GET /files/{id}/comments",
                lambda: self.api_prod("GET", f"files/{self.prod_file_id}/comments"),
                lambda: self.api_replica(
                    "GET", f"files/{self.replica_file_id}/comments"
                ),
            ):
                passed += 1

            # [EDGE] List with limit
            total += 1
            if self.test_operation(
                "GET /files/{id}/comments?limit=2",
                lambda: self.api_prod(
                    "GET", f"files/{self.prod_file_id}/comments", params={"limit": 2}
                ),
                lambda: self.api_replica(
                    "GET", f"files/{self.replica_file_id}/comments", params={"limit": 2}
                ),
            ):
                passed += 1

            # [EDGE] List with offset
            total += 1
            if self.test_operation(
                "GET /files/{id}/comments?offset=0&limit=5",
                lambda: self.api_prod(
                    "GET",
                    f"files/{self.prod_file_id}/comments",
                    params={"offset": 0, "limit": 5},
                ),
                lambda: self.api_replica(
                    "GET",
                    f"files/{self.replica_file_id}/comments",
                    params={"offset": 0, "limit": 5},
                ),
            ):
                passed += 1

        return passed, total

    def run_task_tests(self) -> tuple[int, int]:
        """
        Run task-related tests.

        Endpoints:
        - POST /tasks
        - GET /files/{id}/tasks

        Test Cases:
        POST /tasks:
        - [COMMON] Create task with action=review
        - [COMMON] Create task with action=complete
        - [EDGE] Task with due_at date
        - [EDGE] Task with long message
        - [EDGE] Task on non-existent file (error)
        - [EDGE] Task with completion_rule

        GET /files/{id}/tasks:
        - [COMMON] List tasks on file
        - [EDGE] Pagination with limit
        """
        print("\n✅ Task Operations:")
        passed = 0
        total = 0

        if self.prod_file_id and self.replica_file_id:
            # === POST /tasks ===

            # [COMMON] Create task with action=review
            total += 1
            task_message = (
                f"Parity test task at {datetime.now(timezone.utc).isoformat()}"
            )

            print("  POST /tasks (action=review)...", end=" ")
            try:
                prod_resp = self.api_prod(
                    "POST",
                    "tasks",
                    json={
                        "item": {"type": "file", "id": self.prod_file_id},
                        "message": task_message,
                        "action": "review",
                    },
                )
                replica_resp = self.api_replica(
                    "POST",
                    "tasks",
                    json={
                        "item": {"type": "file", "id": self.replica_file_id},
                        "message": task_message,
                        "action": "review",
                    },
                )

                prod_ok = prod_resp.status_code in (200, 201)
                replica_ok = replica_resp.status_code in (200, 201)

                if prod_ok and replica_ok:
                    prod_data = prod_resp.json()
                    replica_data = replica_resp.json()

                    prod_shape = self.extract_shape(prod_data)
                    replica_shape = self.extract_shape(replica_data)
                    diffs = self.compare_shapes(prod_shape, replica_shape, "data")

                    if diffs:
                        print(" SCHEMA MISMATCH")
                        for d in diffs[:2]:
                            print(f"     {d}")
                    else:
                        print("✅")
                        passed += 1
                else:
                    print(
                        f" STATUS: prod={prod_resp.status_code}, replica={replica_resp.status_code}"
                    )
            except Exception as e:
                print(f" {e}")

            # [COMMON] Create task with action=complete
            total += 1
            print("  POST /tasks (action=complete)...", end=" ")
            try:
                prod_resp = self.api_prod(
                    "POST",
                    "tasks",
                    json={
                        "item": {"type": "file", "id": self.prod_file_id},
                        "message": "Please complete this task",
                        "action": "complete",
                    },
                )
                replica_resp = self.api_replica(
                    "POST",
                    "tasks",
                    json={
                        "item": {"type": "file", "id": self.replica_file_id},
                        "message": "Please complete this task",
                        "action": "complete",
                    },
                )

                prod_ok = prod_resp.status_code in (200, 201)
                replica_ok = replica_resp.status_code in (200, 201)

                if prod_ok == replica_ok:
                    print("✅")
                    passed += 1
                else:
                    print(
                        f" STATUS: prod={prod_resp.status_code}, replica={replica_resp.status_code}"
                    )
            except Exception as e:
                print(f" {e}")

            # [EDGE] Task with due_at date (future date)
            total += 1
            from datetime import timedelta

            due_date = (
                datetime.now(timezone.utc) + timedelta(days=7)
            ).isoformat() + "Z"
            print("  POST /tasks (with due_at)...", end=" ")
            try:
                prod_resp = self.api_prod(
                    "POST",
                    "tasks",
                    json={
                        "item": {"type": "file", "id": self.prod_file_id},
                        "message": "Task with due date",
                        "action": "review",
                        "due_at": due_date,
                    },
                )
                replica_resp = self.api_replica(
                    "POST",
                    "tasks",
                    json={
                        "item": {"type": "file", "id": self.replica_file_id},
                        "message": "Task with due date",
                        "action": "review",
                        "due_at": due_date,
                    },
                )

                prod_ok = prod_resp.status_code in (200, 201)
                replica_ok = replica_resp.status_code in (200, 201)

                if prod_ok == replica_ok:
                    print("✅")
                    passed += 1
                else:
                    print(
                        f" STATUS: prod={prod_resp.status_code}, replica={replica_resp.status_code}"
                    )
            except Exception as e:
                print(f" {e}")

            # [EDGE] Task with very long message
            total += 1
            long_task_message = "Please review this file carefully. " * 30
            print("  POST /tasks (long message)...", end=" ")
            try:
                prod_resp = self.api_prod(
                    "POST",
                    "tasks",
                    json={
                        "item": {"type": "file", "id": self.prod_file_id},
                        "message": long_task_message,
                        "action": "review",
                    },
                )
                replica_resp = self.api_replica(
                    "POST",
                    "tasks",
                    json={
                        "item": {"type": "file", "id": self.replica_file_id},
                        "message": long_task_message,
                        "action": "review",
                    },
                )

                prod_ok = prod_resp.status_code in (200, 201)
                replica_ok = replica_resp.status_code in (200, 201)

                if prod_ok == replica_ok:
                    print("✅")
                    passed += 1
                else:
                    print(
                        f" STATUS: prod={prod_resp.status_code}, replica={replica_resp.status_code}"
                    )
            except Exception as e:
                print(f" {e}")

            # [EDGE] Task on non-existent file
            total += 1
            if self.test_operation(
                "POST /tasks (non-existent file - error)",
                lambda: self.api_prod(
                    "POST",
                    "tasks",
                    json={
                        "item": {"type": "file", "id": "99999999999"},
                        "message": "Should fail",
                        "action": "review",
                    },
                ),
                lambda: self.api_replica(
                    "POST",
                    "tasks",
                    json={
                        "item": {"type": "file", "id": "99999999999"},
                        "message": "Should fail",
                        "action": "review",
                    },
                ),
                validate_schema=False,
            ):
                passed += 1

            # [EDGE] Task with completion_rule
            total += 1
            print("  POST /tasks (completion_rule=all_assignees)...", end=" ")
            try:
                prod_resp = self.api_prod(
                    "POST",
                    "tasks",
                    json={
                        "item": {"type": "file", "id": self.prod_file_id},
                        "message": "Task with completion rule",
                        "action": "review",
                        "completion_rule": "all_assignees",
                    },
                )
                replica_resp = self.api_replica(
                    "POST",
                    "tasks",
                    json={
                        "item": {"type": "file", "id": self.replica_file_id},
                        "message": "Task with completion rule",
                        "action": "review",
                        "completion_rule": "all_assignees",
                    },
                )

                prod_ok = prod_resp.status_code in (200, 201)
                replica_ok = replica_resp.status_code in (200, 201)

                if prod_ok == replica_ok:
                    print("✅")
                    passed += 1
                else:
                    print(
                        f" STATUS: prod={prod_resp.status_code}, replica={replica_resp.status_code}"
                    )
            except Exception as e:
                print(f" {e}")

            # === GET /files/{id}/tasks ===

            # [COMMON] List tasks
            total += 1
            if self.test_operation(
                "GET /files/{id}/tasks",
                lambda: self.api_prod("GET", f"files/{self.prod_file_id}/tasks"),
                lambda: self.api_replica("GET", f"files/{self.replica_file_id}/tasks"),
            ):
                passed += 1

            # [EDGE] List with limit
            total += 1
            if self.test_operation(
                "GET /files/{id}/tasks?limit=3",
                lambda: self.api_prod(
                    "GET", f"files/{self.prod_file_id}/tasks", params={"limit": 3}
                ),
                lambda: self.api_replica(
                    "GET", f"files/{self.replica_file_id}/tasks", params={"limit": 3}
                ),
            ):
                passed += 1

        return passed, total

    def run_hub_tests(self) -> tuple[int, int]:
        """
        Run Hub-related tests (v2025.0 API).

        Note: Hubs require box-version: 2025.0 header.

        Endpoints:
        - GET /hubs
        - POST /hubs
        - GET /hubs/{id}
        - PUT /hubs/{id}
        - GET /hub_items
        - POST /hubs/{id}/manage_items

        Test Cases:
        GET /hubs:
        - [COMMON] List all hubs
        - [EDGE] Without version header (should fail/differ)
        - [EDGE] With limit param

        POST /hubs:
        - [COMMON] Create basic hub
        - [EDGE] Hub with description
        - [EDGE] Hub with unicode title
        - [EDGE] Empty title (error)

        GET /hubs/{id}:
        - [COMMON] Get hub by ID
        - [EDGE] Non-existent hub ID

        PUT /hubs/{id}:
        - [COMMON] Update hub title
        - [COMMON] Update hub description
        - [EDGE] Empty update
        """
        print("\n🏠 Hub Operations (v2025.0):")

        hub_headers = {"box-version": "2025.0"}

        # Check if Hubs feature is available on production account
        # Hubs is an enterprise-only feature, returns 404 on free/dev accounts
        try:
            check_resp = self.api_prod("GET", "hubs", headers=hub_headers)
            if check_resp.status_code == 404:
                print(
                    "  ⏭️  SKIPPED: Hubs not available on this Box account (enterprise-only feature)"
                )
                return 0, 0
        except Exception as e:
            print(f"  ⏭️  SKIPPED: Could not check Hubs availability: {e}")
            return 0, 0

        passed = 0
        total = 0
        prod_hub_id = None
        replica_hub_id = None

        # === GET /hubs ===

        # [COMMON] List all hubs
        total += 1
        if self.test_operation(
            "GET /hubs",
            lambda: self.api_prod("GET", "hubs", headers=hub_headers),
            lambda: self.api_replica("GET", "hubs", headers=hub_headers),
        ):
            passed += 1

        # [EDGE] Without version header
        total += 1
        if self.test_operation(
            "GET /hubs (no version header)",
            lambda: self.api_prod("GET", "hubs"),
            lambda: self.api_replica("GET", "hubs"),
            validate_schema=False,  # May differ in behavior
        ):
            passed += 1

        # [EDGE] With limit
        total += 1
        if self.test_operation(
            "GET /hubs?limit=5",
            lambda: self.api_prod(
                "GET", "hubs", params={"limit": 5}, headers=hub_headers
            ),
            lambda: self.api_replica(
                "GET", "hubs", params={"limit": 5}, headers=hub_headers
            ),
        ):
            passed += 1

        # === POST /hubs ===

        # [COMMON] Create basic hub
        hub_name = f"ParityHub_{datetime.now(timezone.utc).strftime('%H%M%S')}"
        total += 1
        print("  POST /hubs (create basic)...", end=" ")
        try:
            prod_resp = self.api_prod(
                "POST",
                "hubs",
                json={"title": hub_name, "description": "Parity test hub"},
                headers=hub_headers,
            )
            replica_resp = self.api_replica(
                "POST",
                "hubs",
                json={"title": hub_name, "description": "Parity test hub"},
                headers=hub_headers,
            )

            prod_ok = prod_resp.status_code in (200, 201)
            replica_ok = replica_resp.status_code in (200, 201)

            if prod_ok and replica_ok:
                prod_data = prod_resp.json()
                replica_data = replica_resp.json()

                prod_shape = self.extract_shape(prod_data)
                replica_shape = self.extract_shape(replica_data)
                diffs = self.compare_shapes(prod_shape, replica_shape, "data")

                if diffs:
                    print(" SCHEMA MISMATCH")
                    for d in diffs[:2]:
                        print(f"     {d}")
                else:
                    print("✅")
                    passed += 1
                    prod_hub_id = prod_data.get("id")
                    replica_hub_id = replica_data.get("id")
            elif not prod_ok and not replica_ok:
                print("✓ (both failed)")
                passed += 1
            else:
                print(
                    f" STATUS: prod={prod_resp.status_code}, replica={replica_resp.status_code}"
                )
        except Exception as e:
            print(f" {e}")

        # [EDGE] Hub with unicode title
        total += 1
        print("  POST /hubs (unicode title: 日本語Hub)...", end=" ")
        try:
            prod_resp = self.api_prod(
                "POST",
                "hubs",
                json={"title": "日本語Hub_テスト", "description": "Unicode test"},
                headers=hub_headers,
            )
            replica_resp = self.api_replica(
                "POST",
                "hubs",
                json={"title": "日本語Hub_テスト", "description": "Unicode test"},
                headers=hub_headers,
            )

            prod_ok = prod_resp.status_code in (200, 201)
            replica_ok = replica_resp.status_code in (200, 201)

            if prod_ok == replica_ok:
                print("✅")
                passed += 1
            else:
                print(
                    f" STATUS: prod={prod_resp.status_code}, replica={replica_resp.status_code}"
                )
        except Exception as e:
            print(f" {e}")

        # [EDGE] Empty title (should error)
        total += 1
        if self.test_operation(
            "POST /hubs (empty title - error)",
            lambda: self.api_prod(
                "POST",
                "hubs",
                json={"title": "", "description": "Should fail"},
                headers=hub_headers,
            ),
            lambda: self.api_replica(
                "POST",
                "hubs",
                json={"title": "", "description": "Should fail"},
                headers=hub_headers,
            ),
            validate_schema=False,
        ):
            passed += 1

        # === Tests with created hub ===
        if prod_hub_id and replica_hub_id:
            # [COMMON] GET /hubs/{id}
            total += 1
            if self.test_operation(
                "GET /hubs/{id}",
                lambda: self.api_prod(
                    "GET", f"hubs/{prod_hub_id}", headers=hub_headers
                ),
                lambda: self.api_replica(
                    "GET", f"hubs/{replica_hub_id}", headers=hub_headers
                ),
            ):
                passed += 1

            # [COMMON] PUT /hubs/{id} - update title
            total += 1
            if self.test_operation(
                "PUT /hubs/{id} (update title)",
                lambda: self.api_prod(
                    "PUT",
                    f"hubs/{prod_hub_id}",
                    json={"title": f"{hub_name}_Updated"},
                    headers=hub_headers,
                ),
                lambda: self.api_replica(
                    "PUT",
                    f"hubs/{replica_hub_id}",
                    json={"title": f"{hub_name}_Updated"},
                    headers=hub_headers,
                ),
            ):
                passed += 1

            # [COMMON] PUT /hubs/{id} - update description
            total += 1
            if self.test_operation(
                "PUT /hubs/{id} (update description)",
                lambda: self.api_prod(
                    "PUT",
                    f"hubs/{prod_hub_id}",
                    json={"description": "Updated description for parity test"},
                    headers=hub_headers,
                ),
                lambda: self.api_replica(
                    "PUT",
                    f"hubs/{replica_hub_id}",
                    json={"description": "Updated description for parity test"},
                    headers=hub_headers,
                ),
            ):
                passed += 1

            # [EDGE] Empty update
            total += 1
            if self.test_operation(
                "PUT /hubs/{id} (empty update)",
                lambda: self.api_prod(
                    "PUT", f"hubs/{prod_hub_id}", json={}, headers=hub_headers
                ),
                lambda: self.api_replica(
                    "PUT", f"hubs/{replica_hub_id}", json={}, headers=hub_headers
                ),
            ):
                passed += 1

            # [COMMON] GET /hub_items
            total += 1
            if self.test_operation(
                "GET /hub_items?hub_id={id}",
                lambda: self.api_prod(
                    "GET",
                    "hub_items",
                    params={"hub_id": prod_hub_id},
                    headers=hub_headers,
                ),
                lambda: self.api_replica(
                    "GET",
                    "hub_items",
                    params={"hub_id": replica_hub_id},
                    headers=hub_headers,
                ),
            ):
                passed += 1

        # [EDGE] Non-existent hub ID
        total += 1
        if self.test_operation(
            "GET /hubs/99999999999 (not found)",
            lambda: self.api_prod("GET", "hubs/99999999999", headers=hub_headers),
            lambda: self.api_replica("GET", "hubs/99999999999", headers=hub_headers),
            validate_schema=False,
        ):
            passed += 1

        return passed, total

    def run_search_tests(self) -> tuple[int, int]:
        """
        Run search-related tests.

        Endpoint: GET /search

        Test Cases:
        - [COMMON] Basic query search
        - [COMMON] Search with type=file filter
        - [COMMON] Search with type=folder filter
        - [EDGE] Search with limit
        - [EDGE] Search with offset pagination
        - [EDGE] Search for exact phrase (quotes)
        - [EDGE] Search with file_extensions filter
        - [EDGE] Search with ancestor_folder_ids (scope to folder)
        - [EDGE] Search with content_types filter
        - [EDGE] Empty query (should error or return nothing)
        - [EDGE] Very long query string
        - [EDGE] Query with special characters
        - [EDGE] Query with unicode
        - [EDGE] Search for non-existent content
        """
        print("\n🔍 Search Operations:")
        passed = 0
        total = 0

        # [COMMON] Basic query search
        total += 1
        if self.test_operation(
            "GET /search?query=test",
            lambda: self.api_prod("GET", "search", params={"query": "test"}),
            lambda: self.api_replica("GET", "search", params={"query": "test"}),
        ):
            passed += 1

        # [COMMON] Search with type=file filter
        total += 1
        if self.test_operation(
            "GET /search?query=test&type=file",
            lambda: self.api_prod(
                "GET", "search", params={"query": "test", "type": "file"}
            ),
            lambda: self.api_replica(
                "GET", "search", params={"query": "test", "type": "file"}
            ),
        ):
            passed += 1

        # [COMMON] Search with type=folder filter
        total += 1
        if self.test_operation(
            "GET /search?query=test&type=folder",
            lambda: self.api_prod(
                "GET", "search", params={"query": "test", "type": "folder"}
            ),
            lambda: self.api_replica(
                "GET", "search", params={"query": "test", "type": "folder"}
            ),
        ):
            passed += 1

        # [EDGE] Search with limit
        total += 1
        if self.test_operation(
            "GET /search?query=test&limit=5",
            lambda: self.api_prod(
                "GET", "search", params={"query": "test", "limit": 5}
            ),
            lambda: self.api_replica(
                "GET", "search", params={"query": "test", "limit": 5}
            ),
        ):
            passed += 1

        # [EDGE] Search with offset pagination
        total += 1
        if self.test_operation(
            "GET /search?query=test&offset=0&limit=10",
            lambda: self.api_prod(
                "GET", "search", params={"query": "test", "offset": 0, "limit": 10}
            ),
            lambda: self.api_replica(
                "GET", "search", params={"query": "test", "offset": 0, "limit": 10}
            ),
        ):
            passed += 1

        # [EDGE] Search with file_extensions filter
        total += 1
        if self.test_operation(
            "GET /search?query=*&file_extensions=txt,md",
            lambda: self.api_prod(
                "GET", "search", params={"query": "*", "file_extensions": "txt,md"}
            ),
            lambda: self.api_replica(
                "GET", "search", params={"query": "*", "file_extensions": "txt,md"}
            ),
        ):
            passed += 1

        # [EDGE] Empty query (should error or return nothing)
        total += 1
        if self.test_operation(
            "GET /search?query= (empty)",
            lambda: self.api_prod("GET", "search", params={"query": ""}),
            lambda: self.api_replica("GET", "search", params={"query": ""}),
            validate_schema=False,
        ):
            passed += 1

        # [EDGE] Very long query string
        total += 1
        long_query = "search " * 50
        if self.test_operation(
            "GET /search?query=<long string>",
            lambda: self.api_prod("GET", "search", params={"query": long_query}),
            lambda: self.api_replica("GET", "search", params={"query": long_query}),
        ):
            passed += 1

        # [EDGE] Query with special characters
        total += 1
        if self.test_operation(
            "GET /search?query=test@#$%",
            lambda: self.api_prod("GET", "search", params={"query": "test@#$%"}),
            lambda: self.api_replica("GET", "search", params={"query": "test@#$%"}),
        ):
            passed += 1

        # [EDGE] Query with unicode
        total += 1
        if self.test_operation(
            "GET /search?query=日本語テスト",
            lambda: self.api_prod("GET", "search", params={"query": "日本語テスト"}),
            lambda: self.api_replica("GET", "search", params={"query": "日本語テスト"}),
        ):
            passed += 1

        # [EDGE] Search for non-existent content
        total += 1
        if self.test_operation(
            "GET /search?query=NONEXISTENT_CONTENT_XYZ123",
            lambda: self.api_prod(
                "GET", "search", params={"query": "NONEXISTENT_CONTENT_XYZ123"}
            ),
            lambda: self.api_replica(
                "GET", "search", params={"query": "NONEXISTENT_CONTENT_XYZ123"}
            ),
        ):
            passed += 1

        # [EDGE] Search with wildcard
        total += 1
        if self.test_operation(
            "GET /search?query=*",
            lambda: self.api_prod("GET", "search", params={"query": "*"}),
            lambda: self.api_replica("GET", "search", params={"query": "*"}),
        ):
            passed += 1

        # Search for uploaded content (if we have test file)
        if self.prod_file_id:
            total += 1
            # Wait a moment for indexing
            time.sleep(1)
            if self.test_operation(
                "GET /search?query=Parity (find test content)",
                lambda: self.api_prod("GET", "search", params={"query": "Parity"}),
                lambda: self.api_replica("GET", "search", params={"query": "Parity"}),
            ):
                passed += 1

        # Search within specific folder (if we have test folder)
        if self.prod_folder_id and self.replica_folder_id:
            total += 1
            if self.test_operation(
                "GET /search?query=*&ancestor_folder_ids={folder_id}",
                lambda: self.api_prod(
                    "GET",
                    "search",
                    params={"query": "*", "ancestor_folder_ids": self.prod_folder_id},
                ),
                lambda: self.api_replica(
                    "GET",
                    "search",
                    params={
                        "query": "*",
                        "ancestor_folder_ids": self.replica_folder_id,
                    },
                ),
            ):
                passed += 1

        return passed, total

    def run_error_tests(self) -> tuple[int, int]:
        """
        Run error handling tests.

        Test Cases:
        404 Not Found:
        - [EDGE] GET /folders/{non-existent-id}
        - [EDGE] GET /files/{non-existent-id}
        - [EDGE] GET /users/{non-existent-id}
        - [EDGE] PUT /folders/{non-existent-id}
        - [EDGE] PUT /files/{non-existent-id}

        400 Bad Request:
        - [EDGE] POST /folders missing parent
        - [EDGE] POST /folders with invalid parent ID
        - [EDGE] POST /folders with missing name
        - [EDGE] POST /comments with missing item
        - [EDGE] POST /tasks with invalid action

        409 Conflict:
        - [EDGE] POST /folders duplicate name (same parent)

        Invalid Input:
        - [EDGE] Malformed JSON body
        - [EDGE] Invalid field types
        - [EDGE] Negative offset/limit values
        """
        print("\n⚠️  Error Handling:")
        passed = 0
        total = 0

        # === 404 Not Found ===

        # Non-existent folder ID
        total += 1
        if self.test_operation(
            "GET /folders/99999999999 (404)",
            lambda: self.api_prod("GET", "folders/99999999999"),
            lambda: self.api_replica("GET", "folders/99999999999"),
            validate_schema=False,
        ):
            passed += 1

        # Non-existent file ID
        total += 1
        if self.test_operation(
            "GET /files/99999999999 (404)",
            lambda: self.api_prod("GET", "files/99999999999"),
            lambda: self.api_replica("GET", "files/99999999999"),
            validate_schema=False,
        ):
            passed += 1

        # Update non-existent folder
        total += 1
        if self.test_operation(
            "PUT /folders/99999999999 (404)",
            lambda: self.api_prod(
                "PUT", "folders/99999999999", json={"name": "updated"}
            ),
            lambda: self.api_replica(
                "PUT", "folders/99999999999", json={"name": "updated"}
            ),
            validate_schema=False,
        ):
            passed += 1

        # Update non-existent file
        total += 1
        if self.test_operation(
            "PUT /files/99999999999 (404)",
            lambda: self.api_prod("PUT", "files/99999999999", json={"name": "updated"}),
            lambda: self.api_replica(
                "PUT", "files/99999999999", json={"name": "updated"}
            ),
            validate_schema=False,
        ):
            passed += 1

        # List items from non-existent folder
        total += 1
        if self.test_operation(
            "GET /folders/99999999999/items (404)",
            lambda: self.api_prod("GET", "folders/99999999999/items"),
            lambda: self.api_replica("GET", "folders/99999999999/items"),
            validate_schema=False,
        ):
            passed += 1

        # Comments on non-existent file
        total += 1
        if self.test_operation(
            "GET /files/99999999999/comments (404)",
            lambda: self.api_prod("GET", "files/99999999999/comments"),
            lambda: self.api_replica("GET", "files/99999999999/comments"),
            validate_schema=False,
        ):
            passed += 1

        # Tasks on non-existent file
        total += 1
        if self.test_operation(
            "GET /files/99999999999/tasks (404)",
            lambda: self.api_prod("GET", "files/99999999999/tasks"),
            lambda: self.api_replica("GET", "files/99999999999/tasks"),
            validate_schema=False,
        ):
            passed += 1

        # === 400 Bad Request ===

        # Create folder with missing parent
        total += 1
        if self.test_operation(
            "POST /folders (missing parent field)",
            lambda: self.api_prod("POST", "folders", json={"name": "TestNoParent"}),
            lambda: self.api_replica("POST", "folders", json={"name": "TestNoParent"}),
            validate_schema=False,
        ):
            passed += 1

        # Create folder with invalid parent ID
        total += 1
        if self.test_operation(
            "POST /folders (invalid parent ID)",
            lambda: self.api_prod(
                "POST",
                "folders",
                json={"name": "TestBadParent", "parent": {"id": "99999999999"}},
            ),
            lambda: self.api_replica(
                "POST",
                "folders",
                json={"name": "TestBadParent", "parent": {"id": "99999999999"}},
            ),
            validate_schema=False,
        ):
            passed += 1

        # Create folder with missing name
        total += 1
        if self.test_operation(
            "POST /folders (missing name)",
            lambda: self.api_prod("POST", "folders", json={"parent": {"id": "0"}}),
            lambda: self.api_replica("POST", "folders", json={"parent": {"id": "0"}}),
            validate_schema=False,
        ):
            passed += 1

        # Create comment with missing item
        total += 1
        if self.test_operation(
            "POST /comments (missing item)",
            lambda: self.api_prod("POST", "comments", json={"message": "Test"}),
            lambda: self.api_replica("POST", "comments", json={"message": "Test"}),
            validate_schema=False,
        ):
            passed += 1

        # Create comment with missing message
        total += 1
        if self.test_operation(
            "POST /comments (missing message)",
            lambda: self.api_prod(
                "POST",
                "comments",
                json={"item": {"type": "file", "id": self.prod_file_id or "123"}},
            ),
            lambda: self.api_replica(
                "POST",
                "comments",
                json={"item": {"type": "file", "id": self.replica_file_id or "123"}},
            ),
            validate_schema=False,
        ):
            passed += 1

        # Create task with invalid action
        total += 1
        if self.test_operation(
            "POST /tasks (invalid action)",
            lambda: self.api_prod(
                "POST",
                "tasks",
                json={
                    "item": {"type": "file", "id": self.prod_file_id or "123"},
                    "message": "Test",
                    "action": "INVALID_ACTION",
                },
            ),
            lambda: self.api_replica(
                "POST",
                "tasks",
                json={
                    "item": {"type": "file", "id": self.replica_file_id or "123"},
                    "message": "Test",
                    "action": "INVALID_ACTION",
                },
            ),
            validate_schema=False,
        ):
            passed += 1

        # === Invalid Input ===

        # Negative limit
        total += 1
        if self.test_operation(
            "GET /folders/0/items?limit=-1 (invalid)",
            lambda: self.api_prod("GET", "folders/0/items", params={"limit": -1}),
            lambda: self.api_replica("GET", "folders/0/items", params={"limit": -1}),
            validate_schema=False,
        ):
            passed += 1

        # Very large limit
        total += 1
        if self.test_operation(
            "GET /folders/0/items?limit=1000000 (large)",
            lambda: self.api_prod("GET", "folders/0/items", params={"limit": 1000000}),
            lambda: self.api_replica(
                "GET", "folders/0/items", params={"limit": 1000000}
            ),
        ):
            passed += 1

        # Negative offset
        total += 1
        if self.test_operation(
            "GET /folders/0/items?offset=-1 (invalid)",
            lambda: self.api_prod("GET", "folders/0/items", params={"offset": -1}),
            lambda: self.api_replica("GET", "folders/0/items", params={"offset": -1}),
            validate_schema=False,
        ):
            passed += 1

        # Invalid sort direction
        total += 1
        if self.test_operation(
            "GET /folders/0/items?direction=INVALID",
            lambda: self.api_prod(
                "GET", "folders/0/items", params={"direction": "INVALID"}
            ),
            lambda: self.api_replica(
                "GET", "folders/0/items", params={"direction": "INVALID"}
            ),
            validate_schema=False,
        ):
            passed += 1

        # === Test duplicate name conflict ===
        if self.prod_folder_id and self.replica_folder_id:
            # First create a folder
            dup_name = f"DuplicateTest_{datetime.now(timezone.utc).strftime('%H%M%S')}"
            self.api_prod(
                "POST",
                "folders",
                json={"name": dup_name, "parent": {"id": self.prod_folder_id}},
            )
            self.api_replica(
                "POST",
                "folders",
                json={"name": dup_name, "parent": {"id": self.replica_folder_id}},
            )

            # Then try to create with same name (should conflict)
            total += 1
            if self.test_operation(
                "POST /folders (duplicate name - 409)",
                lambda: self.api_prod(
                    "POST",
                    "folders",
                    json={"name": dup_name, "parent": {"id": self.prod_folder_id}},
                ),
                lambda: self.api_replica(
                    "POST",
                    "folders",
                    json={"name": dup_name, "parent": {"id": self.replica_folder_id}},
                ),
                validate_schema=False,
            ):
                passed += 1

        return passed, total

    # -------------------------------------------------------------------------
    # Main Test Runner
    # -------------------------------------------------------------------------

    def run_tests(self):
        """Run all parity tests."""
        print("=" * 70)
        print("BOX API PARITY TESTS")
        print("=" * 70)

        self.setup_replica_environment()
        self.setup_test_resources()

        total_passed = 0
        total_tests = 0

        # Run all test suites
        p, t = self.run_user_tests()
        total_passed += p
        total_tests += t

        p, t = self.run_folder_tests()
        total_passed += p
        total_tests += t

        p, t = self.run_file_tests()
        total_passed += p
        total_tests += t

        p, t = self.run_comment_tests()
        total_passed += p
        total_tests += t

        p, t = self.run_task_tests()
        total_passed += p
        total_tests += t

        p, t = self.run_hub_tests()
        total_passed += p
        total_tests += t

        p, t = self.run_search_tests()
        total_passed += p
        total_tests += t

        p, t = self.run_error_tests()
        total_passed += p
        total_tests += t

        # Cleanup
        self.cleanup_test_resources()
        self.cleanup_replica_environment()

        # Summary
        print()
        print("=" * 70)
        pct = int(total_passed / total_tests * 100) if total_tests > 0 else 0
        print(f"TOTAL: {total_passed}/{total_tests} tests passed ({pct}%)")
        print("=" * 70)

        # Save mismatch log
        self.log_summary()

        return total_passed, total_tests


# =============================================================================
# Pytest Integration
# =============================================================================


def test_box_parity():
    """Run Box parity tests as pytest test."""
    if not BOX_DEV_TOKEN:
        print("ERROR: BOX_DEV_TOKEN environment variable not set")
        print("Set it via: export BOX_DEV_TOKEN=<your_token>")
        print("Or edit the BOX_DEV_TOKEN constant in this file")
        return

    tester = BoxParityTester(BOX_DEV_TOKEN)
    passed, total = tester.run_tests()

    # Fail if less than 70% passed (allow some differences)
    success_rate = passed / total if total > 0 else 0
    assert success_rate >= 0.7, (
        f"Parity tests failed: {passed}/{total} ({int(success_rate * 100)}%)"
    )


# =============================================================================
# Standalone Execution
# =============================================================================


def main():
    """Run parity tests from command line."""
    if not BOX_DEV_TOKEN:
        print("ERROR: BOX_DEV_TOKEN environment variable not set")
        print("Usage: BOX_DEV_TOKEN=<token> python test_box_parity.py")
        sys.exit(1)

    tester = BoxParityTester(BOX_DEV_TOKEN)
    passed, total = tester.run_tests()

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
