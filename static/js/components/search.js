import Service from '../core/service.js'
import { Posts, newsletter_icons, categories } from './content.js'


let search = document.getElementById('search')

document.addEventListener('keydown', async (event) => {
    // If the search element is selected the keys Escape, ArrowUp
    // and ArrowDown can allow you to exit the input, the Enter
    // key makes a request and the "s" key allows you to access
    // search element if search element is not focused.
    if (document.activeElement === search) {
        if (event.code === 'Escape' || event.code === 'ArrowUp' || event.code === 'ArrowDown') {
            search.blur()
        }
        else if (event.code == 'Enter') {
            // This code send request
            console.log('Sending request.')
            let service = new Service('http://localhost:5000/api/post/');
            let response = await service.sendRequest('GET');
            let data = await response.posts
            for (let index = 0; index < data.length; index++) {
                const postData = data[index];
                // Update element if element != new element
                if (Posts.state['data'][index] !== postData) {
                    let authorHTML = data.author != '' ? '' : '<div class="key">' + postData.author + '</div>'
                    Posts.state['data'][index] = postData
                    Posts.state['childs'][index].innerHTML = `
                    <a id="post-${index}" class="content" href="/post/${postData.id}">
                        <img src="${newsletter_icons[postData.newsletter_id]}">
                        <div class="information">
                            <p>${postData.title}</p>
                            <span style="font-size:14px;">${postData.description}</span>
                            <div class="information-atributes">
                                <div class="key">${categories[0]}</div>
                                <div class="key">${postData.datetime.substring(0, 9)}</div>
                                ${authorHTML}
                            </div>
                        </div>
                    </a>`
                }
            }
            search.blur()
        }
        else {
            search.focus()
        }
    } else {
        if (event.code === 'KeyS') {
            search.focus()
            search.value = search.value.substring(0, search.value.length - 2)
        }
    }
})