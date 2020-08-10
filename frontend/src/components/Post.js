import React from 'react';
import {Avatar,  Card} from 'antd';
import { HeartFilled, HeartTwoTone, UserOutlined} from '@ant-design/icons';

function Post({ post, handleLike }) {
    const { author, caption, location, photo, tag_set, is_like } = post;
    const {username, name, avatar_url} = author;

    return (
        <div>
            <Card
                hoverable
                cover={<img src={photo} alt={caption} />}
                actions={[
                    is_like ? <HeartTwoTone twoToneColor="#eb2f96" onClick={()=>handleLike({post, isLike: false})} /> 
                    : <HeartFilled onClick={()=>handleLike({post, isLike: true})} />
                ]}
            >
                <Card.Meta 
                // FIXME: host지정을 로직으로 처리
                avatar={
                    <Avatar size="large" 
                            icon={<img src={`http://localhost:8000` + avatar_url} alt={username} />} 
                    />
                } 
                title={location} 
                description={caption} 
                />
            </Card>
            {/* <img src={photo} alt={caption} style={{ width: "100px" }} /> {caption} {location} */}
        </div>
    )
}

export default Post;