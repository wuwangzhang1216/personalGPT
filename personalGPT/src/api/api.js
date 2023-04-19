
const base_url = "http://127.0.0.1:5000"

// fetch an api call to to get conversation by id
export const getConversation = async (id) => {
    try {
        const response = await fetch(`${base_url}/conversation/${id}`, {
            method: "GET",
            headers: new Headers({
                'Content-Type': 'application/json',
              }),
        })
        return response
    }
    catch (error) {
        console.log(error)
    }
}

// fetch an api call to get all conversations
export const getAllConversations = async () => {
    try {
        const response = await fetch(`${base_url}/conversations`, {
            method: "GET",
            headers: new Headers({
                'Content-Type': 'application/json',
              }),
        })
        let data = await response.json()
        return data
    }
    catch (error) {
        console.log(error)
    }
}


// fetch an api call to change the conversation name
export const changeConversationName = async (id, name) => {
    try {
        const response = await fetch(`${base_url}/conversation/${id}/name`, {
            method: "PUT",
            headers: new Headers({
                'Content-Type': 'application/json',
                }),
            body: JSON.stringify(name)
        })
        return response
    }
    catch (error) {
        console.log(error)
    }
}


// fetch an api call to create a new conversation
export const createConversation = async (conversation) => {
    try {
        const response = await fetch(`${base_url}/conversation`, {
            method: "POST",
            headers: new Headers({
                'Content-Type': 'application/json',
              }),
            body: JSON.stringify(conversation)
        })
        return response
    }
    catch (error) {
        console.log(error)
    }
}


// fetch an api call to update a conversation by id
export const updateConversation = async (id, conversation) => {
    try {
        const response = await fetch(`${base_url}/conversation/${id}`, {
            method: "PUT",
            headers: new Headers({
                'Content-Type': 'application/json',
              }),
            body: JSON.stringify(conversation)
        })
        return response
    }
    catch (error) {
        console.log(error)
    }
}

// fetch an api call to delete a conversation by id
export const deleteConversation = async (id) => {
    try {
        const response = await fetch(`${base_url}/conversation/${id}`, {
            method: "DELETE",
            headers: new Headers({
                'Content-Type': 'application/json',
              }),
        })
        return response
    }
    catch (error) {
        console.log(error)
    }
}

// fetch an api call to download a conversation by id
export const downloadConversation = async (id) => {
    window.open(`${base_url}/conversation/${id}/download`, '_blank');
}