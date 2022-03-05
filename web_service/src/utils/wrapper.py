from http import HTTPStatus

def get_response(err: bool, msg: str, data: dict[str, any] = None, status_code: int = HTTPStatus.OK):
	ret = {
		"error": err,
		"message": msg
	}
	if data:
		ret["data"] = data
	return ret, status_code