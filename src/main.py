if __name__ == "__main__":
    import uvicorn

    # TODO log config
    uvicorn.run("contracts.webapp.app:app", host="0.0.0.0", port=8080, reload=True)
