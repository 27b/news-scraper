import Component from './core/component.js'
import Service from './core/service.js'


const newsletter_icons = [
    /* Notice */ 'https://upload.wikimedia.org/wikipedia/commons/thu…1200px-Corredor_naranja_cordoba_argentina.svg.png',
    /* NYTimes */ 'https://yt3.ggpht.com/a/AATXAJyDX6fn6odU9KqLzyz1jmr6Sf2suzpO0z07ofGTew=s900-c-k-c0xffffffff-no-rj-mo',
    /* Time */ 'https://api.time.com/wp-content/themes/time2014/img/time-logo-og.png',
    /* WashingtonPost */ 'https://play-lh.googleusercontent.com/JDrO88srYGmqrOeyqtT1al3JQD0IKRS-OO7PDMjETiPuDNgCC45wJF8LIBH-QOcTMTE'
]


let posts = new Component("content-list")

posts.onEvent('load', async () => {
    let service = new Service('http://localhost:5000/api/post/');
    let response = await service.sendRequest('GET');
    let data = await response.posts
    console.log(data.length)

    for (var i = 0; i <= data.length; i++) {
        let postItem = data[i] 
        let postComponent = `
            <a class="content" href="/post/${postItem.id}">
                <img src="${newsletter_icons[postItem.newsletter_id]}">
                <div class="information">
                    <p>${postItem.title}</p>
                    <p style="font-size:12px;">${postItem.description}</p>
                    <div class="information-atributes">
                        <div class="key">${postItem.datetime.substring(0, 9)}</div>
                    </div>
                </div>
            </a>
        `
        posts.insert(postComponent)
    }   
})

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