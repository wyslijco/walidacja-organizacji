"""
Tests for SlugConflictValidator.
"""

from validators import SlugConflictValidator


class TestSlugConflictValidator:
    """Test slug conflict validation."""

    def test_no_conflicts_with_valid_slugs(self):
        """Test that valid slugs pass without conflicts."""
        validator = SlugConflictValidator("adres")

        files_to_check = ["org1.yaml", "org2.yaml"]
        all_organizations = {
            "test-org-1": "org1.yaml",
            "test-org-2": "org2.yaml",
            "other-org": "org3.yaml",
        }

        is_valid, errors = validator.validate_conflicts(
            files_to_check, all_organizations
        )

        assert is_valid
        assert len(errors) == 0

    def test_reserved_slug_conflict_detected(self):
        """Test that reserved slug conflicts are detected."""
        validator = SlugConflictValidator("adres")

        files_to_check = ["info_org.yaml"]
        all_organizations = {
            "info": "info_org.yaml",  # Reserved slug
            "test-org": "test.yaml",
        }

        is_valid, errors = validator.validate_conflicts(
            files_to_check, all_organizations
        )

        assert not is_valid
        assert len(errors) == 1
        assert "Zarezerwowany adres 'info' używany w pliku info_org.yaml" in errors[0]

    def test_multiple_reserved_slug_conflicts(self):
        """Test that multiple reserved slug conflicts are detected."""
        validator = SlugConflictValidator("adres")

        files_to_check = ["info_org.yaml", "organizacje_org.yaml"]
        all_organizations = {
            "info": "info_org.yaml",
            "organizacje": "organizacje_org.yaml",
            "test-org": "test.yaml",
        }

        is_valid, errors = validator.validate_conflicts(
            files_to_check, all_organizations
        )

        assert not is_valid
        assert len(errors) == 2
        assert any("Zarezerwowany adres 'info'" in error for error in errors)
        assert any("Zarezerwowany adres 'organizacje'" in error for error in errors)

    def test_reserved_slug_404_detected(self):
        """Test that '404' reserved slug is detected."""
        validator = SlugConflictValidator("adres")

        files_to_check = ["404_org.yaml"]
        all_organizations = {"404": "404_org.yaml"}

        is_valid, errors = validator.validate_conflicts(
            files_to_check, all_organizations
        )

        assert not is_valid
        assert "Zarezerwowany adres '404'" in errors[0]

    def test_no_conflict_when_file_not_being_checked(self):
        """Test that reserved slugs in non-checked files don't trigger errors."""
        validator = SlugConflictValidator("adres")

        files_to_check = ["safe_org.yaml"]  # Only checking this file
        all_organizations = {
            "info": "info_org.yaml",  # Reserved slug, but not being checked
            "safe-org": "safe_org.yaml",
        }

        is_valid, errors = validator.validate_conflicts(
            files_to_check, all_organizations
        )

        assert is_valid
        assert len(errors) == 0

    def test_custom_slug_field_name(self):
        """Test validator with custom slug field name."""
        validator = SlugConflictValidator("slug")  # Different field name

        files_to_check = ["org.yaml"]
        all_organizations = {"info": "org.yaml"}

        is_valid, errors = validator.validate_conflicts(
            files_to_check, all_organizations
        )

        assert not is_valid
        assert "Zarezerwowany slug 'info'" in errors[0]  # Should use custom field name

    def test_empty_files_to_check(self):
        """Test behavior with empty files to check."""
        validator = SlugConflictValidator("adres")

        files_to_check = []
        all_organizations = {
            "info": "info_org.yaml",  # Reserved but not being checked
            "test-org": "test.yaml",
        }

        is_valid, errors = validator.validate_conflicts(
            files_to_check, all_organizations
        )

        assert is_valid
        assert len(errors) == 0

    def test_empty_organizations_list(self):
        """Test behavior with empty organizations list."""
        validator = SlugConflictValidator("adres")

        files_to_check = ["org.yaml"]
        all_organizations = {}  # Empty

        is_valid, errors = validator.validate_conflicts(
            files_to_check, all_organizations
        )

        assert is_valid
        assert len(errors) == 0

    def test_case_sensitive_reserved_slugs(self):
        """Test that reserved slug matching is case-sensitive."""
        validator = SlugConflictValidator("adres")

        files_to_check = ["Info_org.yaml"]
        all_organizations = {
            "Info": "Info_org.yaml"  # Capitalized - should not match reserved "info"
        }

        is_valid, errors = validator.validate_conflicts(
            files_to_check, all_organizations
        )

        # Should pass because "Info" != "info"
        assert is_valid
        assert len(errors) == 0


class TestSlugConflictValidatorWithLists:
    """Test slug conflict validation with list slugs."""

    def test_list_slug_with_reserved_conflict(self):
        """Test that reserved slug in a list is detected."""
        validator = SlugConflictValidator("adres")

        files_to_check = ["org.yaml"]
        all_organizations = {
            "valid-slug": "org.yaml",
            "info": "org.yaml",  # Reserved slug in the same file
            "another-valid": "org.yaml",
        }

        is_valid, errors = validator.validate_conflicts(
            files_to_check, all_organizations
        )

        assert not is_valid
        assert len(errors) == 1
        assert "Zarezerwowany adres 'info' używany w pliku org.yaml" in errors[0]

    def test_list_slug_with_multiple_reserved_conflicts(self):
        """Test that multiple reserved slugs in a list are detected."""
        validator = SlugConflictValidator("adres")

        files_to_check = ["org.yaml"]
        all_organizations = {
            "valid-slug": "org.yaml",
            "info": "org.yaml",  # Reserved
            "organizacje": "org.yaml",  # Reserved
            "404": "org.yaml",  # Reserved
        }

        is_valid, errors = validator.validate_conflicts(
            files_to_check, all_organizations
        )

        assert not is_valid
        assert len(errors) == 3
        assert any("Zarezerwowany adres 'info'" in error for error in errors)
        assert any("Zarezerwowany adres 'organizacje'" in error for error in errors)
        assert any("Zarezerwowany adres '404'" in error for error in errors)

    def test_list_slug_no_conflicts(self):
        """Test that list of valid slugs passes without conflicts."""
        validator = SlugConflictValidator("adres")

        files_to_check = ["org.yaml"]
        all_organizations = {
            "slug-1": "org.yaml",
            "slug-2": "org.yaml",
            "slug-3": "org.yaml",
            "other-org": "other.yaml",
        }

        is_valid, errors = validator.validate_conflicts(
            files_to_check, all_organizations
        )

        assert is_valid
        assert len(errors) == 0

    def test_mixed_list_and_single_slugs(self):
        """Test validation with mix of list and single slug organizations."""
        validator = SlugConflictValidator("adres")

        files_to_check = ["list_org.yaml", "single_org.yaml"]
        all_organizations = {
            "slug-1": "list_org.yaml",  # List slug
            "slug-2": "list_org.yaml",  # List slug
            "single-slug": "single_org.yaml",  # Single slug
            "info": "list_org.yaml",  # Reserved in list
        }

        is_valid, errors = validator.validate_conflicts(
            files_to_check, all_organizations
        )

        assert not is_valid
        assert len(errors) == 1
        assert "Zarezerwowany adres 'info' używany w pliku list_org.yaml" in errors[0]

    def test_list_slug_reserved_not_being_checked(self):
        """Test that reserved slugs in list of non-checked files don't trigger errors."""
        validator = SlugConflictValidator("adres")

        files_to_check = ["safe_org.yaml"]
        all_organizations = {
            "safe-slug-1": "safe_org.yaml",
            "safe-slug-2": "safe_org.yaml",
            "info": "other_org.yaml",  # Reserved but in different file not being checked
            "organizacje": "other_org.yaml",  # Reserved but not being checked
        }

        is_valid, errors = validator.validate_conflicts(
            files_to_check, all_organizations
        )

        assert is_valid
        assert len(errors) == 0
