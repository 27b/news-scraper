import Service from '../core/service.js'
import { Blobs } from './blobs.js'
import { Posts, newsletter_icons, categories } from './content.js'


let search = document.getElementById('search')

document.addEventListener('keydown', async (event) => {
    // If the search element is selected the keys Escape, ArrowUp
    // and ArrowDown can allow you to exit the input, the Enter
    // key makes a request and the "s" key allows you to access
    // search element if search element is not focused.
    if (document.activeElement === search) {
        if (event.code === 'Enter') {
            let service = new Service(`http://localhost:5000/api/post/?title=${search.value}`)
            let response = await service.sendRequest('GET')
            let data = await response.posts
            let childrens = Posts.HTMLElement.children.length - 1;
            
            Blobs.sendWords(search.value)

            // Step 1: Delete old elements
            for (let index = childrens; index !== 0; index--) {
                let post = Posts.HTMLElement.children[index]
                post.remove()
            }

            // Step 2: Create new elements
            for (let index = 0; index < data.length; index++) {
            
                if (data.length === 0) {
                    console.log('Data values index is equal to 0.')
                    break
                }

                let postData = data[index]
                let postComponent = `
                <a id="post-${index}" class="content" href="${postData.url}">
                    <img src="${newsletter_icons[postData.newsletter_id]}">
                    <div class="information">
                        <p>${postData.title}</p>
                        <span class="information-description">${postData.description}</span>
                        <div class="information-atributes">
                            <div class="key">${categories[postData.category_id]}</div>
                            <div class="key">${postData.datetime.split(' ')[0]}</div>
                            ${postData.author !== '' ? '' : '<div class="key">' + postData.author + '</div>'}
                        </div>
                    </div>
                </a>`
                Posts.insert(postComponent)
            }
        }
        else if (event.code === 'Escape' || event.code === 'ArrowUp' || event.code === 'ArrowDown') {
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