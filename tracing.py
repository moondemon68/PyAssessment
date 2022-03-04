import contextlib
import io
from trace import Trace
from symbolic.loader import Loader

# get visited lines
def traceApp(app: Loader, cases: dict) -> list:
	lines = []
	for key in cases:
		tracer = Trace()
		case = dict((x, y) for x, y in key)
		with contextlib.redirect_stdout(io.StringIO()):
			tracer.runfunc(app._getFunc(), **case)
			r = tracer.results()
			for _, lineno in r.counts:
				lines.append(lineno)
	lines = list(set(lines))
	return lines