import React, { useState } from "react";

import ProfileSection from "./ProfileSection";
import cx from "classnames";

import styles from "./UserProfile.module.css"

const countWordsLeft = (str) => {
    return maxWords - str.trim().split(/\s+/).length;
};


const maxWords = 250;

export const ProfileBio = ({ bio, onChange, readonly, required }) => {
    const [wordsLeft, setWordsLeft] = useState(countWordsLeft(bio));
    const onChangeText = (e) => {
        const num = countWordsLeft(e.target.value);
        if (num >= 0) {
            setWordsLeft(num);
            if (onChange) {
                onChange(e);
            }
        }
    };

    return (
        <ProfileSection header="Bio">
            <textarea id="bioField" rows="10" value={bio} name="bio" readOnly={readonly} className={cx({ "form-control": !readonly, "form-control-plaintext": readonly, "required": required })} onChange={onChangeText}></textarea>
            {!readonly && <div className={styles["word-count-text"]}>- {wordsLeft} words left</div>}
        </ProfileSection>
    );
};

export default ProfileBio;