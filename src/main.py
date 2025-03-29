if __name__ == "__main__":
    import uvicorn

    from contracts.common.settings import settings

    # TODO log config
    uvicorn.run(
        "contracts.webapp.app:app",
        host=settings.webapp_host,
        port=settings.webapp_port,
        reload=True,
    )
