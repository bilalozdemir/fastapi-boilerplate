import logging

from src.main import app
from src.helpers.config_helper import APP_CONFIG

if __name__ == '__main__':
    import uvicorn
    logging.info(f"Running with configs:\n{APP_CONFIG.json()}")

    if APP_CONFIG.sentry_integration:
        import sentry_sdk
        sentry_sdk.init(
            dsn=APP_CONFIG.sentry_dsn,
            debug=APP_CONFIG.debug,
            environment=APP_CONFIG.sentry_env,
        )

        app = SentryAsgiMiddleware(app)

    logging_level = "info" if not APP_CONFIG.debug else "debug"

    uvicorn.run(
        "src.main:app",
        host=APP_CONFIG.host,
        port=APP_CONFIG.port,
        log_level=logging_level,
        debug=APP_CONFIG.debug,
        reload=APP_CONFIG.auto_reload
    )
