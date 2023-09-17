import React from "react";
import ProfileSection from "./ProfileSection";
import TextField from "./forms/TextField";
import { formatDate } from "../../utils";
import FormLabelField from "./forms/FormLabelField";
import styles from "./UserProfile.module.css"
import cx from "classnames";

export const ProfileDetail = ({ date_joined, role_teams=[], status }) => {
    return (
        <ProfileSection header="Member Details">
            <div className="py-2">Member since {formatDate(date_joined)}</div>
            <FormLabelField id="profileStatus" label="Status" required={false} readonly={true}>
                <i className={cx("fas fa-star", styles["status-icon"] , styles[status === 'ACTIVE' ? "status-icon-active" :"status-icon-inactive"])}></i>
                <span className={styles["member-info-text"]}>
                    {status.toLowerCase()}
                </span>
            </FormLabelField>

            {role_teams.map((team, index) => {
                return <div key={"team_role_" + index}>
                    <TextField id={"p_team_role_" + index} label="Role" type="text" readonly={true} value={team.role_name}></TextField>
                    <TextField id={"p_team_" + index} label="Team" type="text" readonly={true} value={team.team_name}></TextField>
                </div>
            })}
        </ProfileSection>
    );
};

export default ProfileDetail;