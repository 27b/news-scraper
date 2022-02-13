/**
 * This component is used to create the service logic.
 */
export default class Service {

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
    sendRequest(method) {
        try {
            let request = new Request(this.url, {method: method})
            fetch(request)
                .then(response => {
                    if(!response.ok) {
                        console.log('Request failed with status', response.status)
                    }
                    return response.json()
                })
                .then(data => {
                    return data
                })
        } catch (error) {
            console.log('ERROR:', error)
        }
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
