import React from 'react';
import ProfileImage from "../../images/ProfileImage.png";
import styles from "./MemberImage.module.css";


const MemberImage = ({profile}) => {
  console.log(profile.photo)
  const imageSrc = profile.photo === "" ? ProfileImage : profile.photo
  return (
      <img
        alt="Profiles"
        src={imageSrc}
        className={styles["img-size"]}
      />
  )
}

export default MemberImage
