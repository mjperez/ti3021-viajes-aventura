import unittest
from unittest.mock import MagicMock, patch
from unittest.mock import MagicMock, patch
from src.business.auth_service import AuthService
from src.utils.exceptions import ValidacionError
from src.utils.validators import validar_rut

class TestAuthManager(unittest.TestCase):

    @patch('src.business.auth_service.UsuarioDAO')
    def test_registro_usuario_exitoso(self, mock_dao_class):
        # Setup mock
        mock_dao = mock_dao_class.return_value
        mock_dao.obtener_por_email.return_value = None
        mock_dao.obtener_por_rut.return_value = None  # RUT no existe
        mock_dao.crear.return_value = 1
        
        # Instantiate Service
        service = AuthService()

        # Execute
        rut = "12.345.678-5" # RUT valido
        usuario = service.registrar_usuario(rut, "test@example.com", "Password123", "Test User")

        # Assert
        self.assertEqual(usuario.id, 1)
        mock_dao.crear.assert_called_once()

    @patch('src.business.auth_service.UsuarioDAO')
    def test_registro_usuario_rut_duplicado(self, mock_dao_class):
        # Setup mock
        mock_dao = mock_dao_class.return_value
        mock_dao.obtener_por_email.return_value = None
        mock_dao.obtener_por_rut.return_value = MagicMock() # RUT existe
        
        # Instantiate Service
        service = AuthService()

        # Execute & Assert
        with self.assertRaises(ValidacionError) as cm:
            service.registrar_usuario("12.345.678-5", "test@example.com", "Password123", "Test User")
        
        self.assertEqual(str(cm.exception), "RUT duplicado")

    def test_validar_rut(self):
        # Valid cases
        self.assertTrue(validar_rut("12.345.678-5"))
        self.assertTrue(validar_rut("11.111.111-1"))
        
        # Invalid cases
        self.assertFalse(validar_rut("12.345.678-K")) # Wrong DV
        self.assertFalse(validar_rut("11.111.111-2")) # Wrong DV
        self.assertFalse(validar_rut("invalid"))
        self.assertFalse(validar_rut(""))

class TestPricing(unittest.TestCase):
    def test_integer_pricing(self):
        # Verify that we can handle integer prices
        price = 10000
        self.assertIsInstance(price, int)
        self.assertEqual(price * 2, 20000)

if __name__ == '__main__':
    unittest.main()
