import React from "react";
import cx from "classnames";
import FormLabelField from "./FormLabelField";

const TextField = ({ id, label, value="", name="", onChange, readonly=false, required=false, type="text", placeholder="" }) => {
  return (
    <FormLabelField id={id} label={label} readonly={readonly} required={required}>
      <input type={type} name={name} className={cx({ "form-control": !readonly, "form-control-plaintext": readonly, "required": required })} id={id} placeholder={placeholder} readOnly={readonly} value={value} onChange={onChange}></input>
    </FormLabelField>
  );
};

export default TextField;