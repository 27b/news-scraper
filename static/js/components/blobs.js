import Component from '../core/component.js'
import Service from '../core/service.js'


export var Blobs = new Component('blobs')

Blobs.HTMLElement.searchText = ''

async function getBlobs(searchText) {
    let url = 'http://localhost:5000/api/blob/'
    if (searchText) url = `http://localhost:5000/api/blob/?words=${searchText}`
    let service = new Service(url)
    let response = await service.sendRequest('GET')
    let data = await response.blobs

    Blobs.HTMLElement.replaceChildren(); // Delete old elements
    
    for (let i = 0; i < data.length; i++) {
        Blobs.insert(`<div class="key">${data[i]}</div>`)
    }
}

Blobs.onEvent('load', async () => {
    getBlobs()
})


Blobs.sendWords = async (words) => {
    console.log(words)
    getBlobs(words)
}


export default { Blobs };
