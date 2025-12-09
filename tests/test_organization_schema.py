"""
Tests for OrganizationSchemaValidator.
"""

from validators import OrganizationSchemaValidator


class TestOrganizationSchemaValidator:
    """Test organization schema validation."""

    def test_valid_organization_passes(self, mock_krs_client, valid_organization_data):
        """Test that valid organization data passes validation."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)

        is_valid, errors = validator.validate_structure(valid_organization_data)

        assert is_valid
        assert len(errors) == 0

    def test_empty_data_fails(self, mock_krs_client):
        """Test that empty data fails validation."""
        validator = OrganizationSchemaValidator("adres", mock_krs_client)

        is_valid, errors = validator.validate_structure({})

        assert not is_valid
        assert "Pusty plik YAML" in errors

    def test_missing_required_fields(
        self, mock_krs_client, organization_missing_fields
    ):
        """Test that missing required fields are detected."""
        validator = OrganizationSchemaValidator("adres", mock_krs_client)

        is_valid, errors = validator.validate_structure(organization_missing_fields)

        assert not is_valid
        assert any("Brakuje wymaganego pola: adres" in error for error in errors)
        assert any("Brakuje wymaganego pola: strona" in error for error in errors)
        assert any("Brakuje wymaganego pola: krs" in error for error in errors)
        assert any("Brakuje wymaganego pola: dostawa" in error for error in errors)
        assert any("Brakuje wymaganego pola: produkty" in error for error in errors)

    def test_invalid_krs_format(self, mock_krs_client):
        """Test that invalid KRS format is detected."""
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": "test",
            "strona": "https://test.org",
            "krs": "123",  # Invalid - too short
            "dostawa": {
                "ulica": "test",
                "kod": "12-345",
                "miasto": "test",
                "telefon": "123456789",
            },
            "produkty": [{"nazwa": "test", "link": "https://test.com"}],
        }

        is_valid, errors = validator.validate_structure(data)

        assert not is_valid
        assert any("Nieprawidłowy format KRS" in error for error in errors)

    def test_invalid_slug_format(self, mock_krs_client):
        """Test that invalid slug format is detected."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": "INVALID-SLUG!",  # Invalid characters
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {
                "ulica": "test",
                "kod": "12-345",
                "miasto": "test",
                "telefon": "123456789",
            },
            "produkty": [{"nazwa": "test", "link": "https://test.com"}],
        }

        is_valid, errors = validator.validate_structure(data)

        assert not is_valid
        assert any("Nieprawidłowy format adres" in error for error in errors)

    def test_empty_slug(self, mock_krs_client):
        """Test that empty slug is detected."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": "",  # Empty slug
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {
                "ulica": "test",
                "kod": "12-345",
                "miasto": "test",
                "telefon": "123456789",
            },
            "produkty": [{"nazwa": "test", "link": "https://test.com"}],
        }

        is_valid, errors = validator.validate_structure(data)

        assert not is_valid
        assert any("musi być niepustym ciągiem znaków" in error for error in errors)

    def test_slug_as_list_valid(self, mock_krs_client):
        """Test that slug field as a list of valid strings passes validation."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": ["test-slug-1", "test-slug-2", "test-slug-3"],  # List of slugs
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {
                "ulica": "test",
                "kod": "12-345",
                "miasto": "test",
                "telefon": "123456789",
            },
            "produkty": [{"nazwa": "test", "link": "https://test.com"}],
        }

        is_valid, errors = validator.validate_structure(data)

        assert is_valid
        assert len(errors) == 0

    def test_slug_as_list_with_invalid_format(self, mock_krs_client):
        """Test that invalid slug format in list is detected."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": ["valid-slug", "INVALID-SLUG!", "another-valid"],  # One invalid
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {
                "ulica": "test",
                "kod": "12-345",
                "miasto": "test",
                "telefon": "123456789",
            },
            "produkty": [{"nazwa": "test", "link": "https://test.com"}],
        }

        is_valid, errors = validator.validate_structure(data)

        assert not is_valid
        assert any(
            "Nieprawidłowy format adres: INVALID-SLUG!" in error for error in errors
        )

    def test_slug_as_list_with_empty_string(self, mock_krs_client):
        """Test that empty string in slug list is detected."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": ["valid-slug", "", "another-valid"],  # One empty
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {
                "ulica": "test",
                "kod": "12-345",
                "miasto": "test",
                "telefon": "123456789",
            },
            "produkty": [{"nazwa": "test", "link": "https://test.com"}],
        }

        is_valid, errors = validator.validate_structure(data)

        assert not is_valid
        assert any("musi być niepustym ciągiem znaków" in error for error in errors)

    def test_slug_as_empty_list(self, mock_krs_client):
        """Test that empty list for slug field is handled."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": [],  # Empty list
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {
                "ulica": "test",
                "kod": "12-345",
                "miasto": "test",
                "telefon": "123456789",
            },
            "produkty": [{"nazwa": "test", "link": "https://test.com"}],
        }

        is_valid, errors = validator.validate_structure(data)

        # Empty list should be valid (no slugs to validate)
        assert is_valid
        assert len(errors) == 0

    def test_slug_as_invalid_type(self, mock_krs_client):
        """Test that non-string, non-list slug type is rejected."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": 123,  # Invalid type (number)
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {
                "ulica": "test",
                "kod": "12-345",
                "miasto": "test",
                "telefon": "123456789",
            },
            "produkty": [{"nazwa": "test", "link": "https://test.com"}],
        }

        is_valid, errors = validator.validate_structure(data)

        assert not is_valid
        assert any(
            "musi być ciągiem znaków lub listą ciągów znaków" in error
            for error in errors
        )


class TestDeliveryValidation:
    """Test delivery data validation."""

    def test_empty_delivery_fails(self, mock_krs_client):
        """Test that empty delivery object fails validation."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": "test",
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {},  # Empty delivery
            "produkty": [{"nazwa": "test", "link": "https://test.com"}],
        }

        is_valid, errors = validator.validate_structure(data)

        assert not is_valid
        assert any(
            "Pole dostawa musi być obiektem z wymaganymi polami" in error
            for error in errors
        )

    def test_missing_delivery_fields(self, mock_krs_client):
        """Test that missing delivery fields are detected."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": "test",
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {"ulica": "test"},  # Missing other fields
            "produkty": [{"nazwa": "test", "link": "https://test.com"}],
        }

        is_valid, errors = validator.validate_structure(data)

        assert not is_valid
        assert any(
            "Brakuje wymaganego pola dostawy: dostawa.kod" in error for error in errors
        )
        assert any(
            "Brakuje wymaganego pola dostawy: dostawa.miasto" in error
            for error in errors
        )
        assert any(
            "Brakuje wymaganego pola dostawy: dostawa.telefon" in error
            for error in errors
        )

    def test_empty_delivery_field_values(self, mock_krs_client):
        """Test that empty delivery field values are detected."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": "test",
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {
                "ulica": "",
                "kod": "12-345",
                "miasto": "test",
                "telefon": "123456789",
            },
            "produkty": [{"nazwa": "test", "link": "https://test.com"}],
        }

        is_valid, errors = validator.validate_structure(data)

        assert not is_valid
        assert any("Pole dostawa.ulica nie może być puste" in error for error in errors)

    def test_invalid_postal_code_format(self, mock_krs_client):
        """Test that invalid postal code format is detected."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": "test",
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {
                "ulica": "test",
                "kod": "invalid",
                "miasto": "test",
                "telefon": "123456789",
            },
            "produkty": [{"nazwa": "test", "link": "https://test.com"}],
        }

        is_valid, errors = validator.validate_structure(data)

        assert not is_valid
        assert any("Nieprawidłowy format kodu pocztowego" in error for error in errors)

    def test_invalid_phone_format(self, mock_krs_client):
        """Test that invalid phone format is detected."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": "test",
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {
                "ulica": "test",
                "kod": "12-345",
                "miasto": "test",
                "telefon": "invalid",
            },
            "produkty": [{"nazwa": "test", "link": "https://test.com"}],
        }

        is_valid, errors = validator.validate_structure(data)

        assert not is_valid
        assert any("Nieprawidłowy format numeru telefonu" in error for error in errors)


class TestProductsValidation:
    """Test products validation."""

    def test_empty_product_name(self, mock_krs_client):
        """Test that empty product name is detected."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": "test",
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {
                "ulica": "test",
                "kod": "12-345",
                "miasto": "test",
                "telefon": "123456789",
            },
            "produkty": [{"nazwa": "", "link": "https://test.com"}],  # Empty name
        }

        is_valid, errors = validator.validate_structure(data)

        assert not is_valid
        assert any(
            "produkty[0] pole nazwa nie może być puste" in error for error in errors
        )

    def test_missing_product_link(self, mock_krs_client):
        """Test that missing product link is detected."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": "test",
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {
                "ulica": "test",
                "kod": "12-345",
                "miasto": "test",
                "telefon": "123456789",
            },
            "produkty": [{"nazwa": "Test Product"}],  # Missing link
        }

        is_valid, errors = validator.validate_structure(data)

        assert not is_valid
        assert any(
            "produkty[0] brakuje wymaganego pola: link" in error for error in errors
        )

    def test_empty_product_link(self, mock_krs_client):
        """Test that empty product link is detected."""
        mock_krs_client.set_default_response(True, "")
        validator = OrganizationSchemaValidator("adres", mock_krs_client)
        data = {
            "nazwa": "Test",
            "adres": "test",
            "strona": "https://test.org",
            "krs": "1234567890",
            "dostawa": {
                "ulica": "test",
                "kod": "12-345",
                "miasto": "test",
                "telefon": "123456789",
            },
            "produkty": [{"nazwa": "Test Product", "link": ""}],  # Empty link
        }

        is_valid, errors = validator.validate_structure(data)

        assert not is_valid
        assert any(
            "produkty[0] pole link nie może być puste" in error for error in errors
        )
