import React, {useMemo, useState, useEffect}from 'react';
import {Button, Card} from 'antd';
import Suggestion from './Suggestion'
import useAxios from 'axios-hooks';
import Axios from 'axios';
import {useAppContext} from 'store';
import "./SuggestionList.scss";

export default function SuggestionList({style}) {
    const {store: {jwtToken}} = useAppContext();

    const [userList, setUserList] = useState([]);
    
    const headers = { Authorization: `JWT ${jwtToken}`}
    const [{data: origUserList, loading, error}, refetch] = useAxios({
        url: "http://localhost:8000/accounts/suggestions/",
        headers,
    })
    // 랜더 될때마다 맵핑하기 때문에 비효율적인 로직 => useMemo 훅 사용
    // const userList = origUserList && origUserList.map(user=>({...user, is_follow: false})) 

    // const userList = useMemo(()=> {
    //     if (!origUserList) return []
    //     return origUserList.map(user=>({...user, is_follow: false}))
    // }, [origUserList]) // origUserList가 바뀔 때에만 수행

    useEffect(() => {
        if (!origUserList) setUserList([]);
        else setUserList(origUserList.map(user => ({ ...user, is_follow: false })));
    }, [origUserList]);

    const onFollowUser = (username) => {
        Axios.post('http://localhost:8000/accounts/follow/', {username}, {headers})
        .then(response => {
            setUserList(prevUserList => 
            prevUserList.map(user => 
                user.username !== username ? user : {...user, is_follow: true}    
            )
        )
        })
        .catch(error => {
             console.log(error)
        })
        
    }
    return (
        <div style={style}>
            {loading && <div>loading ...</div>}
            {error && <div>로딩 중에 에러가 발생했습니다.</div>}
            <Button onClick={()=> refetch()}>새로고침</Button>
            <Card title="Suggestions for you" size="small">
                {userList.map(suggestionUser => (
                    <Suggestion 
                        key={suggestionUser.username} 
                        suggestionUser={suggestionUser} 
                        onFollowUser={onFollowUser}
                    />
                ))}
            </Card>
        </div>
    )
}