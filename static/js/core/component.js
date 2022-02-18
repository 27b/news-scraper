/**
 * This component is used to create the component logic.
 */
export default class Component {
    
    /**
     * Create an component.
     * @param {string} identifier 
     */
    constructor(identifier) {
        this.state = {}
        this.identifier = identifier
        this.HTMLElement = document.getElementById(identifier)
    }

    /**
     * Add event to component(.
     * @param {string} string
     * @param {function} callback
     */
    onEvent(event, callback) {
        if (this.HTMLElement) {
            this.HTMLElement.addEventListener(event, callback())
        } else {
            console.log('ERROR: Element identifier error, the identifier is:', this.identifier)
        }
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
