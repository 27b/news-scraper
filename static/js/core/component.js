class Component {
    
    /**
     * Create an component.
     * @param {string} identifier 
     */
    constructor(identifier) {
        this.data = {}
        this.identifier = identifier
        this.HTMLElement = document.getElementById(identifier)
    }

    /**
     * Add event to component.
     * @param {string} string 
     * @param {function} callback 
     */
    onEvent(string, callback){
        this.HTMLElement.addEventListener(string, () => {
            callback()
        })
    }
    
    /**
     * Insert html in component
     * @param {string} html 
     */
    insert(html) {
        this.HTMLElement.innerHTML += html 
    }

    /**
     * Delete component
     */
    delete() {
        this.HTMLElement.remove()    
    }
}
