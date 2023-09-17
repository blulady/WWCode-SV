import React from "react";
import styles from "./UserProfile.module.css";

export const ProfileSection = ({ header, children }) => {

    return (
        <div className="d-flex flex-column py-3">
            <div className={styles["header"]}>{header}</div>
            <hr className={styles["divider"] + " pb-4"}></hr>
            {children}
        </div>
    );
};

export default ProfileSection;