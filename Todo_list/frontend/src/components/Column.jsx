import React from "react";
import styled from "styled-components";

const Container = styled.div`
    margin: 8px;
    border: 1px solid black;
    border-radius: 2px;
    width: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-bottom: 10px;
`;

const Title = styled.div`
    padding: 5px;
`;

const Column = (props) => {
    return (
        <Container>
            <Title>{props.column.title}</Title>
        </Container>
    )
}

export default Column