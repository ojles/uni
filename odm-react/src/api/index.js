class Api {
    constructor(apiUrl) {
        this.apiUrl = apiUrl;
    }

    getObjects = (majorId) => {
        let requestUrl = this.apiUrl + '/objects';
        if (majorId) {
            requestUrl += '?majorId=' + majorId;
        }
        return fetch(requestUrl)
            .then(response => response.json());
    }

    getObjectById = (objectId) => {
        const requestUrl = this.apiUrl + '/objects/' + objectId;
        return fetch(requestUrl)
            .then(response => response.json());
    }

    updateObject = (object) => {
        const requestUrl = this.apiUrl + '/objects';
        return fetch(requestUrl, {
                method: 'POST',
                body: JSON.stringify(object),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json());
    }

    removeObjectById = (objectId) => {
        const requestUrl = this.apiUrl + '/objects/' + objectId;
        return fetch(requestUrl, {
                method: 'DELETE'
            });
    }

    addObject = (newObject) => {
        const requestUrl = this.apiUrl + '/objects';
        return fetch(requestUrl, {
                method: 'PUT',
                body: JSON.stringify(newObject),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json());
    }
}

export default new Api(process.env.REACT_APP_API_URL);
export {Api};
