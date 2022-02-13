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
    async sendRequest(method, contentType='application/json') {
        try {
            let request = new Request(
                this.url,
                {
                    method: method,
                    headers: {
                        'Content-Type': contentType
                    }
                }
            );
            return fetch(request)
            .then(response => {
                if(!response.ok) console.log('Request failed with status', response.status)
                return response.json()
            })
            .then(data => data)
            .catch(error => console.log(error))
        } catch (error) {
            console.log('ERROR:', error)
        }
    }

    /**
     * Get result
     * @returns Data
     */
    async getResponse() {
        // Get response.
        return this.data
    }
}
