// SPDX-FileCopyrightText: Copyright (c) 2017-2024 slowtec GmbH <post@slowtec.de>
// SPDX-License-Identifier: MIT OR Apache-2.0

//! Asynchronous RTU client(master) example

#[tokio::main(flavor = "current_thread")]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    use tokio_serial::SerialStream;

    use tokio_modbus::prelude::*;

    let tty_path = "/dev/ttyUSB0";

    // defines the Modbus slave address, which is set to 0x17 (23 in decimal).
    let slave = Slave(0x17);

    // A serial port is configured to communicate at a baud rate of 19200, and SerialStream::open is used to open the serial port for communication.
    let builder = tokio_serial::new(tty_path, 19200);

    let port = SerialStream::open(&builder).unwrap();

    // This line creates a context (ctx) for Modbus RTU communication that is attached to the specified slave device. 
    let mut ctx = rtu::attach_slave(port, slave);
    println!("Reading a sensor value");
    
    // 1. sends a request to the slave device at address 0x17 to read 2 holding registers starting from the register address 0x082B.
    // 2. The response (rsp) contains the values read from the specified holding registers, which are then printed. 
    let rsp = ctx.read_holding_registers(0x082B, 2).await??;

    println!("Sensor value is: {rsp:?}");

    println!("Disconnecting");
    ctx.disconnect().await?;

    Ok(())
}