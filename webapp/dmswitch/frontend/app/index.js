const React = require('react');
const ReactDOM = require('react-dom');
const Button = require('react-bootstrap/lib/Button');
const NumberFormat = require('react-number-format');


class DmSwitch extends React.Component{
    constructor(props){
        super(props);
        this.state = {otp: "", feedback: ""};
        this.handleChange = this.handleChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }

    handleChange(value){
        this.setState({otp: value.value});
    }

    onSubmit(event){
        var body = new FormData();
        body.append('username', 'fkalter');
        body.append('token', this.state.otp);
        console.log(body);
        fetch('/checkin',
              {method: 'POST', body: body}).then(function(response){
          return response.text();
        }).then(function(bodyText){
            var feedback = '';
            if(bodyText=='invalid'){
                this.setState({tag: 'bg-danger'});
                feedback = 'Invalid otp, please try again.';
            }
            if(bodyText=='valid'){
                this.setState({tag: 'bg-success'});
                feedback = 'Otp accepted, timer is reset.';
            }
            console.log(feedback);
            this.setState({feedback: feedback});
        }.bind(this));
    }

    render(){
        return(
        <div>
            <form className="form-horizontal">
              <div className="form-group">
                <label htmlFor="otp" className="col-md-2 control-label">Otp</label>
                <div className="col-md-6">
                    <NumberFormat id="otp" type="tel" displayType="input" format="### ###" value={this.state.otp} onValueChange={this.handleChange} />
                </div>
              </div>
              <div className="form-group">
                <div className="col-md-offset-2 col-md-6">
                  <button type="button" onClick={this.onSubmit} className="btn btn-default">Submit</button>
                </div>
              </div>

              <div className="form-group">
                <div className="col-md-offset-2 col-md-6">
                  <p className="form-control-static feedback" className={this.state.tag}>{this.state.feedback}</p>
               </div>
              </div>
            </form>
        </div>
        );
    }

}

ReactDOM.render(
  <DmSwitch />,
  document.getElementById('container')
);
