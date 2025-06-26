chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "fetchConfig") {
        sendResponse({}); 
    }
});
