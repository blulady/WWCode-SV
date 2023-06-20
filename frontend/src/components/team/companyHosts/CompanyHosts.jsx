import React from "react";
import Table from "../../common/Table";
import { columns } from "./comapnyHosts.config";
import styles from "./CompanyHosts.index.module.css";

const CompanyHosts = () => {
  const data = [
    {
      id: 1,
      company: "Apple",
      city: "cupertino",
      contacts: [{ name: "Andy", email: "andy@gmail.com" }, { name: "Andy", email: "andy@gmail.com" }],
      notes: "This here is some placeholder text, intended to take up quite a bit of vertical space, to demonstrate how the vertical alignment works in the preceding cells.",
    },
  ];
  return (
    <Table columns={columns} data={data} tableClass={styles["company-hosts-table"]} />
  );
};

export default CompanyHosts;
