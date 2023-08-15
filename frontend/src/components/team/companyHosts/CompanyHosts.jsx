import React from "react";
import GenricTable from "../../common/Table";
import { columns } from "./comapnyHosts.config";
import styles from "./CompanyHosts.index.module.css";

const CompanyHosts = () => {
  const data = [
    {
      id: 1,
      company: "Apple",
      city: "cupertino",
      contacts: [{ name: "Andy Salvation Alexdender", email: "andy@gmail.com", info: "hello test..." }, { name: "Andy", email: "andy@gmail.com", info: "hello test..." }],
      notes: "This here is some placeholder text, intended to take up quite a bit of vertical space, to demonstrate how the vertical alignment works in the preceding cells.",
    },
  ];
  return (
    <GenricTable tableClass={styles["company-hosts-table"]} columns={columns} data={data}  />
  );
};

export default CompanyHosts;
