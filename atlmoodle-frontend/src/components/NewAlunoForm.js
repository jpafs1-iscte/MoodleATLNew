import React from "react";
import { Button, Form, FormGroup, Input, Label } from "reactstrap";

import axios from "axios";

import { API_URL } from "../constants";

class NewAlunoForm extends React.Component {
  state = {
    pk: 0,
    user: "",
    first_name: "",
    last_name: "",
    email:"",
    anoEscolar: "",

  };

  componentDidMount() {
    if (this.props.student) {
      const { pk, user, anoEscolar } = this.props.student;
      this.setState({ pk, user, anoEscolar });
    }
  }

  onChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

  createStudent = e => {
    e.preventDefault();
    axios.post(API_URL, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  editStudent = e => {
    e.preventDefault();
    axios.put(API_URL + this.state.pk, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  defaultIfEmpty = value => {
    return value === "" ? "" : value;
  };

  render() {
    return (
      <Form onSubmit={this.props.student ? this.editStudent : this.createStudent}>
        <FormGroup>
          <Label for="user">User:</Label>
          <Input
            type="text"
            name="user"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.user)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="first_name">Primeiro Nome:</Label>
          <Input
            type="text"
            name="primeironome"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.first_name)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="last_name">Ultimo Nome:</Label>
          <Input
            type="text"
            name="ultimonome"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.last_name)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="email">Email:</Label>
          <Input
            type="email"
            name="contacto"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.email)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="anoEscolar">Ano Escolar:</Label>
          <Input
            type="text"
            name="anoEscolar"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.anoEscolar)}
          />
        </FormGroup>
        <Button>Send</Button>
      </Form>
    );
  }
}

export default NewAlunoForm;