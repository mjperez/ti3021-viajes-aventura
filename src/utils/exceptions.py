"""Excepciones Personalizadas - Manejo de Errores

Define excepciones personalizadas para el sistema.
Facilita el manejo de errores específicos de la aplicación.

Excepciones esperadas:"""

class AutenticacionError(Exception):
    """Error en autenticación (login fallido, token inválido)"""

class ValidacionError(Exception):
    """Error en validación de datos de entrada"""

class ReservaError(Exception):
    """Error en operaciones de reserva (sin cupos, fechas inválidas)"""

class PagoError(Exception):
    """Error en procesamiento de pagos"""

class BaseDatosError(Exception):
    """Error en operaciones de base de datos"""

class PermisoError(Exception):
    """Error de permisos (usuario no autorizado)"""

class RecursoNoEncontradoError(Exception):
    """Error cuando no se encuentra un recurso (404)"""

class CuposAgotadosError(ReservaError):
    """Error específico cuando no hay cupos disponibles"""