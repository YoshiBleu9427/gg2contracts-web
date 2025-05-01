if __name__ == "__main__":
    import uvicorn

    from contracts.common.settings import settings

    uvikwargs = {
        "host": settings.webapp_host,
        "port": settings.webapp_port,
        "reload": settings.debug,
        "workers": settings.webapp_workers,
    }

    if settings.webapp_ssl_certfile:
        uvikwargs["ssl_certfile"] = settings.webapp_ssl_certfile
    if settings.webapp_ssl_keyfile:
        uvikwargs["ssl_keyfile"] = settings.webapp_ssl_keyfile

    uvicorn.run("contracts.webapp.app:app", **uvikwargs)  # type: ignore
