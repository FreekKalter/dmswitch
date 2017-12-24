const React = require('react');

const OtpFormatter = React.createClass({
    render(){
        var otp = this.props.value;
        var first = str.substring(0,3);
        var last  = str.substring(3,6);
        return first + " " + last;
    }
});

module.exports = OtpFormatter;
