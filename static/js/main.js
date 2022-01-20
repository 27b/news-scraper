let posts = new Component(identifier="#posts")

posts.onEvent('init', () => {
    let service = new Service('/post/').sendRequest(method='GET')
    for (i = 0; i < service.length; i++) {
        postItem = service[i]
        postComponent = `
            <a class="content" href="/post/${postItem.id}">
                <img src="${'hello-world'}">
                <div class="information">
                    <p>${postItem.title}</p>
                    <div class="information-atributes">
                        <div class="key">${postItem.url}</div>
                    </div>
                </div>
            </a>
        `
    }
})

posts.onEvent('update', () => {
    let service = new Service('/post/').sendRequest(method='GET')
    for (i = 0; i < service.length; i++) {
        if (posts.data[i].id != service[i].id) {
            // Update data
        }
        else {
            postItem = service[i]
            postComponent = `
                <a class="content" href="/post/${postItem.id}">
                    <img src="${2+2}">
                    <div class="information">
                        <p>${postItem.title}</p>
                        <div class="information-atributes">
                            <div class="key">${postItem.url}</div>
                        </div>
                    </div>
                </a>
            `
        }
    }
})

let buttonModal = new Component(identifier="#button-modal")
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
        let modal = new Component(identifier="#modal")
        
        // Get modal buttonClose for delete modal
        let modalButtonClose = new Component(identifier="#button-close")
        modalButtonClose.onEvent('click', () => {
            // Change data for modal-button to false
            buttonModal.data['use'] = false

            // Delete modal
            modal.delete()
        })
    }
})