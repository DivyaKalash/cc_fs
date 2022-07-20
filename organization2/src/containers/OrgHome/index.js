import React from 'react';
import "./style.css";
import { Navigate } from "react-router-dom";

import { useDispatch, useSelector } from "react-redux";

const OrgHome = () => {
    const auth = useSelector((state) => state.auth);

    const block = useSelector((state) => state.blockchain);
    if (!auth.authenticate) {
        return <Navigate to={"/signin"} />;
      }
    return (
        <div>
            <div class="cont" >
            <div class="container">
                <h2 class="orgName" style={{paddingBottom: "40px", marginTop: "-35px", color: "grey"}}>Organization name: {auth.user.name}</h2>
                <h3 class="orgId" style={{paddingBottom: "40px", color: "grey"}}>Organization Id: {(auth.user._id).slice(-5)}</h3>
                <hr/>
                <div class="box">
                    <div class="icon"><i class="fas fa-address-card"></i>
                    </div>
                    <div class="content">
                        <h1>Card Alloted: {block.alloted_credit}</h1>
                        {/* <h2></h2> */}
                    </div>
                </div>
                <div class="box">
                    <div class="icon"><i class="fas fa-credit-card"></i>
                    </div>
                    <div class="content">
                        <h1>Availabe Credit: {block.available_credit}</h1>
                    </div>
                </div>
                <div class="box">
                    <div class="icon"><i class="fas fa-clipboard-check"></i></div>
                    <div class="content">
                        <h1>Credit Used: {block.credit_used}</h1>
                    </div>
                </div>
            </div>
            </div>
        </div>
    )
}

export default OrgHome;
