import React, {useState, useEffect} from "react";
import styled from "styled-components";
import Column from "./Column";
import axios from "axios";

const Container = styled.div`
    display: flex
`

const Board = (props) => {
    const initial_data = {tasks: {}, columns: {}, columnOrder: {}, taskIds: undefined
    }
    const [board, setBoard] = useState(initial_data)

    useEffect(() => {
        //fetchBoard().then(data => setBoard(data))
        const fetchBoard = async () => {
            const res = await axios.get("http://127.0.0.1:8000/board")
            console.log(res)

        }
        fetchBoard()
    }, [])

    //async function fetchBoard(){
    //    const response = await fetch('/board');
    //    const data = await response.json();
    //    return data.board;
    //}

    return (
        <div>
            {
                Object.values(board.columnOrder).map((columnId, index) => {
                    const column = board.columns[columnId];
                    const tasks = board.taskIds.map(taskIds => board.tasks[taskIds])


                    console.log(tasks)
                    return <Column key={column.id} column={column} tasks={tasks} index={index} />;
                })
                /*Object.values(board.columns).map((columnId, index) => {
                    const column = board.columns[columnId];
                    const tasks = board.taskIds.map(taskIds => board.tasks[taskIds])
                    return (
                        <div>
                            <p>{columnId.}</p>
                        </div>
                    )
                    //return <Column key={column.id} column={column} tasks={tasks} index={index} />
                })*/
            }
        </div>
    )
}

export default Board;