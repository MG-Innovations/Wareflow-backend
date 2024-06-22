from typing import Any, Dict, List

from fastapi.responses import JSONResponse


class ApiResponse:
    @staticmethod
    def response_created(
        message="Resource created",
        code=201,
        success=True,
        data={},
        paginator={},
        exp=(None, None, None),
    ):
        # message = message_format(message)
        data = {
            "message": message,
            "status_code": code,
            "success": success,
            "data": data.dict(),
            "paginator": paginator,
        }
        return JSONResponse(content=data, status_code=code)

    @staticmethod
    def response_ok(
        message="Ok",
        code=200,
        success=True,
        data={},
        paginator={},
        exp=(None, None, None),
    ):
        # message = message_format(message)
        data = {
            "message": message,
            "status_code": code,
            "success": success,
            "data": data,
            "paginator": paginator,
        }
        return JSONResponse(content=data, status_code=code)

    @staticmethod
    def response_internal_server_error(
        message="Internal server error",
        code=500,
        success=False,
        data={},
        paginator={},
        exp=(None, None, None),
        e="",
        attributes={},
    ):
        # message = message_format(message)
        data = {
            "message": message,
            "status_code": code,
            "success": success,
            "data": data,
            "paginator": paginator,
        }

        # send data to newrelic
        # Errors logged can be viewed with context ->
        # APM > {env}-ultron > Errors inbox >selecting error > profile(for context) in the above line,
        # env can be stage, pp, prod
        # error_log_agent.notice_error(error=exp, attributes=attributes)
        return JSONResponse(content=data, status_code=code)

    @staticmethod
    def response_bad_request(
        message="Bad Request",
        code=400,
        success=False,
        data={},
        paginator={},
        exp=(None, None, None),
    ):
        # message = message_format(message)
        data = {
            "message": message,
            "status_code": code,
            "success": success,
            "data": data,
            "paginator": paginator,
        }
        return JSONResponse(content=data, status_code=code)

    @staticmethod
    def response_unprocessable_entity(
        message="Bad Request",
        code=422,
        success=False,
        data={},
        paginator={},
        exp=(None, None, None),
    ):
        # message = message_format(message)
        data = {
            "message": message,
            "status_code": code,
            "success": success,
            "data": data,
            "paginator": paginator,
        }
        return JSONResponse(content=data, status_code=code)

    @staticmethod
    def response_conflict(
        message="Bad Request",
        code=409,
        success=False,
        data={},
        paginator={},
        exp=(None, None, None),
    ):
        # message = message_format(message)
        data = {
            "message": message,
            "status_code": code,
            "success": success,
            "data": data,
            "paginator": paginator,
        }
        return JSONResponse(content=data, status_code=code)

    @staticmethod
    def response_unauthenticate(
        message="Unauthenticate",
        code=401,
        success=False,
        data={},
        paginator={},
        exp=(None, None, None),
    ):
        # message = message_format(message)
        data = {
            "message": message,
            "status_code": code,
            "success": success,
            "data": data,
            "paginator": paginator,
        }
        return JSONResponse(content=data, status_code=code)

    @staticmethod
    def response_unauthorized(
        message="Unauthorized",
        code=403,
        success=False,
        data={},
        paginator={},
        exp=(None, None, None),
    ):
        # message = message_format(message)
        data = {
            "message": message,
            "status_code": code,
            "success": success,
            "data": data,
            "paginator": paginator,
        }
        return JSONResponse(content=data, status_code=code)

    @staticmethod
    def response_not_found(
        message="Not Found",
        code=404,
        success=False,
        data={},
        paginator={},
        exp=(None, None, None),
    ):
        # message = message_format(message)
        data = {
            "message": message,
            "status_code": code,
            "success": success,
            "data": data,
            "paginator": paginator,
        }
        return JSONResponse(content=data, status_code=code)

    @staticmethod
    def response_not_acceptable(
        message="Not acceptable",
        code=406,
        success=False,
        data={},
        paginator={},
        exp=(None, None, None),
    ):
        # message = message_format(message)
        data = {
            "message": message,
            "status_code": code,
            "success": success,
            "data": data,
            "paginator": paginator,
        }
        return JSONResponse(content=data, status_code=code)

    @staticmethod
    def response_conflict_request(
        message="Conflict",
        code=409,
        success=False,
        data={},
        paginator={},
        exp=(None, None, None),
    ):
        # message = message_format(message)
        data = {
            "message": message,
            "status_code": code,
            "success": success,
            "data": data,
            "paginator": paginator,
        }
        return JSONResponse(content=data, status_code=code)