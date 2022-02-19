import Component from '../core/component.js'
import Service from '../core/service.js'


export const newsletter_icons = [
    /* Notice */ 'https://upload.wikimedia.org/wikipedia/commons/thu…1200px-Corredor_naranja_cordoba_argentina.svg.png',
    /* NYTimes */ 'https://yt3.ggpht.com/a/AATXAJyDX6fn6odU9KqLzyz1jmr6Sf2suzpO0z07ofGTew=s900-c-k-c0xffffffff-no-rj-mo',
    /* Time */ 'https://api.time.com/wp-content/themes/time2014/img/time-logo-og.png',
    /* WashingtonPost */ 'https://play-lh.googleusercontent.com/JDrO88srYGmqrOeyqtT1al3JQD0IKRS-OO7PDMjETiPuDNgCC45wJF8LIBH-QOcTMTE'
]

export const categories = [
    null, 'business', 'politics', 'technology', 'science', 'world', 'books',
    'style', 'education', 'health', 'sports', 'arts', 'television', 'climate',
    'automobile'
]

export var Posts = new Component("content-list");

Posts.state['data'] = []
Posts.state['childs'] = []

Posts.onEvent('load', async () => { 
    let service = new Service('http://localhost:5000/api/post/');
    let response = await service.sendRequest('GET');
    let data = await response.posts

    for (var index = 0; index < data.length; index++) {
        let postData = data[index]
        let authorHTML = data.author != '' ? '' : '<div class="key">' + postData.author + '</div>'
        let postComponent = `
            <a id="post-${index}" class="content" href="api/post/${postData.id}">
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
        Posts.insert(postComponent)
        let post = document.getElementById('post-' + index)
        Posts.state['data'].push(postData)
        Posts.state['childs'].push(post)
    }
})

export default { Posts, newsletter_icons, categories };

/*
Posts.onEvent('change', () => {
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
*/