use std::sync::Arc;
use tokio::sync::Mutex;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum TicketError {
    #[error("Ticket wasn't set")]
    NoTicketStored,
    #[error("Invalid ticket")]
    InvalidTicket,
}

pub struct TicketManager {
    current_ticket: Arc<Mutex<Option<String>>>
}

impl TicketManager {
    pub fn new() -> Self {
        Self {
            current_ticket: Arc::new(Mutex::new(None)),
        }
    }

    pub async fn save_ticket(&self, ticket: String) {
        let mut lock = self.current_ticket.lock().await;
        *lock = Some(ticket);
    }

    pub async fn validate_ticket(&self, ticket: &str, delete_after: bool) -> Result<bool, TicketError> {
        let mut lock = self.current_ticket.lock().await;
        let stored = lock.as_ref().ok_or(TicketError::NoTicketStored)?;
        if stored == ticket {
            if delete_after {
                *lock = None;
            }
            Ok(true)
        } else {
            Err(TicketError::InvalidTicket)
        }
    }
}


#[tokio::test]
async fn test_ticket_store() {
    let ticket = "new_test_ticket".to_string();
    let ticket_manager = TicketManager::new();
    ticket_manager.save_ticket(ticket.clone()).await;
    let lock = ticket_manager.current_ticket.lock();
    let stored = lock.await.as_ref().expect("failed to read ref").to_string();
    assert!(ticket == stored);
    // invalid ticket check
    let invalid_ticket = "invalid_ticket".to_string();
    let result_err = ticket_manager.validate_ticket(&invalid_ticket.clone(), false).await;
    assert!(result_err.is_err(), "Invalid ticket");
    // Valid ticket keep 
    let result = ticket_manager.validate_ticket(&ticket.clone(), false).await;
    assert!(result.unwrap());
    // Ticket wasn't deleted
    let lock = ticket_manager.current_ticket.lock();
    assert!(lock.await.is_some());
    // Valid ticket delete
    let result = ticket_manager.validate_ticket(&ticket.clone(), true).await;
    assert!(result.unwrap());
    let lock = ticket_manager.current_ticket.lock();
    assert!(lock.await.is_none());
}

