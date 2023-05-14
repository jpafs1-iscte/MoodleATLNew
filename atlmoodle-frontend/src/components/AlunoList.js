import React, { Component } from "react";
import { Table } from "reactstrap";
import NewAlunoModal from "./NewAlunoModal";

import ConfirmRemovalModal from "./ConfirmRemovalModal";

class AlunoList extends Component {
  render() {
    const students = this.props.students;
    return (
      <Table dark>
        <thead>
          <tr>
            <th>User</th>
            <th>Primeiro Nome</th>
            <th>Ultimo Nome</th>
            <th>Email</th>
            <th>Ano Escolar</th>

          </tr>
        </thead>
        <tbody>
          {!students || students.length <= 0 ? (
            <tr>
              <td colSpan="6" align="center">
                <b>Ops, no one here yet</b>
              </td>
            </tr>
          ) : (
            students.map(student => (
                <tr key={student.pk}>
                <td>{student.user}</td>
                <td>{student.first_name}</td>
                <td>{student.last_name}</td>
                <td>{student.email}</td>
                <td>{student.anoEscolar}</td>
                <td align="center">
                  <NewAlunoModal
                    create={false}
                    student={student}
                    resetState={this.props.resetState}
                  />
                  &nbsp;&nbsp;
                  <ConfirmRemovalModal
                    pk={student.pk}
                    resetState={this.props.resetState}
                  />
                </td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    );
  }
}

export default AlunoList;