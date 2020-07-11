import React, {useEffect, useState} from 'react';
import Axios from 'axios'
import Post from 'components/Post'
const apiUrl = "http://localhost:8000/api/posts/"

function PostList() {
    const [postList, setPostList] = useState([]);

    useEffect(() => {
        Axios.get(apiUrl)
        .then(response => {
            const { data } = response
            console.log('loaded response:', response)
            setPostList(data); 
        }) 
        .catch(error => {
            // error.response;
        })
     console.log('mounted')
    }, []);
    return (
        <div>
            <h1>PostList </h1>
            {postList.map(post => {
                 return <Post post={post} key={post.id} />
            })}
        </div>
    )
}

export default PostList;