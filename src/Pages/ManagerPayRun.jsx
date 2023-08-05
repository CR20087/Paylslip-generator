import React from 'react'
import PayTable from '../Components/PayRun.tsx'
import SideBar from "../Components/Sidebar"
import styled from 'styled-components'
import Footer from '../Components/Footer.jsx'
function EmployeeTimesheets() {

    return (
        <Page>
            <SideBar/>
            <Container>
                <PayTable/>
            </Container>
            <Footer/>
        </Page>
      )
    }
    
    const Page = styled.div`
    display: grid;
    `
    const Container = styled.div`
    .css-80pr5n-MuiPaper-root {width:70vw;}
    .css-1hhu9xl {width:70vw;z-index:1}
    .css-1rs06yn {
        background-color: #4d6788;
        :hover {
            background-color: #2d4965
        }}
    .css-zcbmsk-MuiButtonBase-root-MuiButton-root {
        background-color: #4d6788;
        :hover {
            background-color: #2d4965
        }}

    .mui-box-container-form {
        position: fixed;
        top: 45%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 700;
        background-color: rgba(255, 255, 255, 1);
        height: 40vh;
        padding-bottom: 10rem;
    
        .buttons-for-form {
            height: fit-content;
            padding-top: 3rem;
            float: right;
        }
    }
    .true {
        visibility: visible;
        position:absolute;
        top:0px;
        left: 0px;
        width:100%;
        height:100;
        background-color:black;
        opacity:0.8;
        z-index: 500;
    }
    .false {
        visibility: hidden;
    }
    display: flex;
    flex-direction: column;
    height:fit-content;
    justify-self:center;
    padding-top: 5rem;
    .timesheet-entrys {
        padding-top: 10rem;
    }
`
export default EmployeeTimesheets