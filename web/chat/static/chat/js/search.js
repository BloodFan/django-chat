$("#searchField").keyup(function(e) {
    if (e.keyCode === 13) {
        chatSearch(e)
    }
});

$("#searchButton").click(chatSearch)

function chatSearch (e) {
    var query = $("#searchField").val();
    const url = new URL(window.location);
    url.searchParams.set('search', query);
    window.history.pushState(null, '', url.toString());
    chatList()
}