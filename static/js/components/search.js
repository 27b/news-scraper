let search = document.getElementById('search')

document.addEventListener('keydown', (event) => {
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
            // ...
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