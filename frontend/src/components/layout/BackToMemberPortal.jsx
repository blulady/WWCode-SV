import React from 'react';
import BackButton from "../../images/arrow_back_24px.png";
import styles from "./BackToMemberPortal.module.css";
import { useNavigate } from "react-router-dom";
import { useTeamContext } from '../../context/team/TeamContext';


const BackToMemberPortal = ({teamId, pending}) => {
  const navigate = useNavigate();
  const { teams } = useTeamContext();
  const teamInfo = teams[teamId];
  const teamHome = pending ? "Invitees" : teamInfo.pages[0].label;
  const endpoint = pending ? "/pending" : "/members"

  return (
    <div>
      <button
        className={styles["back-member-btn"]}
        onClick={() => {
          navigate("/team/" + teamId + endpoint);
        }}
      >
        <img
        src={BackButton}
        className={styles["back-btn-img"]}
        alt="Back Button"
      />
      Back to {teamHome}
      </button>
    </div>
  )
}

export default BackToMemberPortal;
