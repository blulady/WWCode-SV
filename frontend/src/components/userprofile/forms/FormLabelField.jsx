import React from "react";
import cx from "classnames";
import common_styles from "./Forms.common.module.css";

const FormLabelField = ({ id, label, readonly=false, required=true, children }) => {
    const wrapperClass = cx("py-2, align-items-center", {"row": readonly}, common_styles["form-label-field"] );
    const labelClass = cx(common_styles["label"], { "form-label": !readonly, "col-form-label col-3": readonly, [common_styles["required"]]: required && !readonly });
    const fieldClass = cx({ "col-9": readonly });
  return (
    <div className={wrapperClass}>
        <label htmlFor={id} className={labelClass}>{label}:</label>
        <div className={fieldClass}>
            {children}
        </div>
    </div>
  );
};

export default FormLabelField;