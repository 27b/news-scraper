/*

let buttonModal = new Component("button-modal")
buttonModal.data['use'] = false

buttonModal.onEvent('click', () => {
    if (buttonModal.data['use'] == false) {
        // Change data of buttonModal
        buttonModal.data['use'] = true

        // Create modal view with closed button
        let createModal = `
            <div id="modal" class="modal">
                <div class="modal-content">
                    <p><button id="button-close">x</button></p>
                </div>
            </div>
        `
        
        // Get modal view
        let modal = new Component(identifier="modal")
        
        // Get modal buttonClose for delete modal
        let modalButtonClose = new Component(identifier="button-close")
        modalButtonClose.onEvent('click', () => {
            // Change data for modal-button to false
            buttonModal.data['use'] = false

            // Delete modal
            modal.delete()
        })
    }
})
*/