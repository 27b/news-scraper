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

Posts.onEvent('load', async () => { 
    let service = new Service('http://localhost:5000/api/post/');
    let response = await service.sendRequest('GET');
    let data = await response.posts

    for (var index = 0; index < data.length; index++) {
        let postData = data[index]
        let postComponent = `
            <a id="post-${index}" class="content" href="api/post/${postData.id}">
                <img src="${newsletter_icons[postData.newsletter_id]}">
                <div class="information">
                    <p>${postData.title}</p>
                    <span class="information-description">${postData.description}</span>
                    <div class="information-atributes">
                        <div class="key">${categories[0]}</div>
                        <div class="key">${postData.datetime.split(' ')[0]}</div>
                        ${data.author !== '' ? '' : '<div class="key">' + postData.author + '</div>'}
                    </div>
                </div>
            </a>`
        Posts.insert(postComponent)
    }
})

export default { Posts, newsletter_icons, categories };
