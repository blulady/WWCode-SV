import React, { useState, useEffect } from "react";
import GenricTable from "../../common/Table";
import WwcApi from '../../../WwcApi'
import { columns } from "./comapnyHosts.config";
import styles from "./CompanyHosts.index.module.css";

const CompanyHosts = () => {
  const [companyHosts, setCompanyHosts] = useState([])

  useEffect(() => {
    const fetchCompanyHost = async () => {
      try {
        const hosts = await WwcApi.getCompanyHost()
        setCompanyHosts(hosts)
      } catch (error) {
        console.log("An error occurred while fetching company hosts:", error)
      }
      fetchCompanyHost()
    }
  }, [])

  // TODO: Currently, there is no data coming from WwcApi.getCompanyHost().
  // The following `companyHosts` data is temporarily used for testing purposes.
  // const companyHosts = [
  //   {
  //     id: 1,
  //     company: "Apple",
  //     city: "cupertino",
  //     contacts: [{ name: "Andy Salvation Alexdender", email: "andy@gmail.com", info: "hello test..." }, { name: "Andy", email: "andy@gmail.com", info: "hello test..." }],
  //     notes: "This here is some placeholder text, intended to take up quite a bit of vertical space, to demonstrate how the vertical alignment works in the preceding cells.",
  //   },
  // ];
  return (
    <GenricTable tableClass={styles["company-hosts-table"]} columns={columns} data={companyHosts}  />
  );
};

export default CompanyHosts;
