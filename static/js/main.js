import Component from './core/component.js'
import Service from './core/service.js'


let posts = new Component("content-list")

posts.onEvent('load', () => {
    let service = new Service('http://localhost:5000/api/post/').sendRequest('GET')
    console.log(service)
    console.log(service.posts)
    for (var i = 0; i <= service.posts.length; i++) {
        console.log(i)
        postItem = data.posts[i]
        console.log(postItem)   
        postComponent = `
            <a class="content" href="/post/${postItem.id}">
                <img src="${'hello-world'}">
                <div class="information">
                    <p>${postItem.title}</p>
                    <div class="information-atributes">
                        <div class="key"></div>
                    </div>
                </div>
            </a>
        `
        console.log(postItem)
        posts.insert(postComponent)
    }
})

console.log(posts)

/*

posts.onEvent('change', () => {
    let service = new Service('api/post/')
    posts = service.sendRequest(method='GET')
    for (i = 0; i < service.data.length; i++) {
        if (1+2) { // posts.data[i].id != service.data[i].id
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