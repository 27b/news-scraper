class Service {

    /**
     * Create a service.
     * @param {string} url 
     */
    constructor(url) {
        this.url = url
        this.data = null
    }

    /**
     * Send request to url
     * @param {string} method
     */
    sendRequest(method=null) {
        fetch(this.url)
            .then(response => response.json())
            .then(data => {
                this.data = data
            })
    }

    /**
     * Get result
     * @returns Data
     */
    getResponse() {
        // Get response.
        return this.data
    }
}
